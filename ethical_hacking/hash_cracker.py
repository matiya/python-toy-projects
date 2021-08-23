#!/usr/bin/env python

import itertools
from hashlib import sha1
import sys
from termcolor import colored
import string


def obtener_lineas(archivo):
    """Generador simple que devuelve lineas del archivo
    Implementado para no cargar un archivo grande
    en memoria

    :param: archivo_diccionario: Archivo con palabras
    """
    with open(archivo, "r") as f:
        line = f.readline()
        while line:
            yield line.strip()
            line = f.readline()


def imprimir_resultados(metodo, texto=None):

    """Imprime el resultado, tanto si encuentra o no encuentra
        el texto plano que produce el hash

    :param texto: Texto plano que produce el hash
    :param metodo: El tipo de comprobación realizada
    :returns: None

    """
    if texto:
        print(
            colored(
                f"[I] Solución encontrada para: {texto} con el método {metodo}",
                "green",
                "on_white",
            )
        )
    else:
        print(
            colored(
                f"[I] Coincidencia no encontrada con {metodo}\n\
                Intentar otro método",
                "red",
                "on_white",
            )
        )
    sys.exit()


class AtaqueDiccionario:
    """Implementa distintos algoritmos para obtener c3olisiones
    contra un hash conocido en base a diccionarios
    """

    def __init__(
        self,
        hash_comprobar,
        archivo_diccionario,
        archivo_complementos=None,
        archivo_intercalado=None,
    ):
        """Ofrece métodos para comprobar un hash
            contra un diccionario

        :param hash_comprobar: El hash que se desea romper
        :param archivo_diccionario: Archivo con palabras a comprobar
        :param archivo_complementos: Archivo con prefijos y sufijos
        :param archivo_intercalado: Archvio con infijos/interfijos
        :returns: Nada

        """
        self.hash_comprobar = hash_comprobar
        self.archivo_diccionario = archivo_diccionario
        self.archivo_complementos = archivo_complementos
        self.archivo_intercalado = archivo_intercalado

    @staticmethod
    def __menu_herramienta():
        opcion = 188
        while opcion < 1 or opcion > 6:
            print(
                """
            MENU\n
              ================================
              1 - Diccionario literal (sin variaciones)
              2 - Minúsculas y mayúsculas
              3 - Palabras transpuestas (permutaciones)
              4 - Prefijos y sufijos
              5 - Símbolos intercalados
              6 - Todas las anteriores
              ================================
            """
            )
            opcion = input("Opción: ")
            opcion = int(opcion)
        return opcion

    def recorrer_diccionario_literal(self):
        """Recorre linea a linea el diccionario
        Comprueba literalmente las palabr
        """
        for linea in obtener_lineas(self.archivo_diccionario):
            sha1_hash = sha1(linea.encode())
            if sha1_hash.hexdigest() == self.hash_comprobar:
                return "Diccionario literal", linea
        return "Diccionario literal", False

    def recorrer_diccionario_minmay(self):
        """Recorre linea a linea el diccionario
        Comprueba las palabras capitalizadas,
        mayúsculas y minúsculas
        """
        for linea in obtener_lineas(self.archivo_diccionario):
            for func in str.lower, str.upper, str.capitalize, str.swapcase:
                linea_transformada = func(linea)
                sha1_hash = sha1(linea_transformada.encode())
                if sha1_hash.hexdigest() == self.hash_comprobar:
                    return "Mayúsculas y minúsculas", linea_transformada
        return "Mayúsculas y minúsculas", False

    def recorrer_diccionario_transpuesto(self):
        """Recorre linea a linea el diccionario
        Comprueba las palabras transpuestas
        ej: abc, acb,cba,bac, etc
        FIXME: Para palabras largas, se come toda la RAM
        """
        for linea in obtener_lineas(self.archivo_diccionario):
            for palabra in ["".join(l) for l in itertools.permutations(linea)]:
                # print("palabra: " + palabra)
                sha1_hash = sha1(palabra.encode())
                if sha1_hash.hexdigest() == self.hash_comprobar:
                    return "Diccionario con permutaciones", palabra
        return "Diccionario con permutaciones", False

    def recorrer_diccionario_complementos(self):
        """Recorre linea a linea el diccionario
        agrega prefijos y sufijos en base al archivo
        self.diccionario_complementos
        """

        if self.archivo_complementos is None:
            self.archivo_complementos = input("Ingrese el archivo con complementos: ")
        for linea in obtener_lineas(self.archivo_diccionario):
            for complemento in obtener_lineas(self.archivo_complementos):
                palabra_prefijo = complemento + linea
                palabra_sufijo = linea + complemento
                sha1_hash_pre = sha1(palabra_prefijo.encode())
                sha1_hash_suf = sha1(palabra_sufijo.encode())
                if sha1_hash_suf.hexdigest() == self.hash_comprobar:
                    return "Diccionario con complementos", palabra_sufijo
                if sha1_hash_pre.hexdigest() == self.hash_comprobar:
                    return "Diccionario con complementos", palabra_prefijo
        return "Diccionario con complementos", False

    def recorrer_diccionario_intercalado(self):
        """Recorre linea a linea el diccionario
        comprueba infijos en base al archivo dado en self.archivo_intercalado
        """
        if self.archivo_intercalado is None:
            self.archivo_intercalado = input("Ingrese el archivo con símbolos: ")

        for linea in obtener_lineas(self.archivo_diccionario):
            for complemento in obtener_lineas(self.archivo_intercalado):
                for i in range(len(linea) + 1):
                    palabra = linea[0:i] + complemento + linea[i::]
                    sha1_hash = sha1(palabra.encode())
                    if sha1_hash.hexdigest() == self.hash_comprobar:
                        return "Diccionario con símbolos intercalados", palabra
        return "Diccionario con símbolos intercalados", False

    def recorrer_diccionario_full(self):
        """Llama a las funciones antes definidas

        Ofrece un TUI para elegir el tipo de ataque y
        los archivos
        """
        opcion = self.__menu_herramienta()

        if self.hash_comprobar is None:
            self.hash_comprobar = input("Ingrese el hash a comprobar")
            self.hash_comprobar = self.hash_comprobar.strip()
        if self.archivo_diccionario is None:
            self.archivo_diccionario = input("Ingrese el archivo de diccionario: ")

        if opcion == 1:
            metodo, resultado = self.recorrer_diccionario_literal()

        elif opcion == 2:
            metodo, resultado = self.recorrer_diccionario_minmay()

        elif opcion == 3:
            metodo, resultado = self.recorrer_diccionario_transpuesto()

        elif opcion == 4:
            metodo, resultado = self.recorrer_diccionario_complementos()

        elif opcion == 5:
            metodo, resultado = self.recorrer_diccionario_intercalado()

        elif opcion == 6:
            for estrategia in [
                self.recorrer_diccionario_literal,
                self.recorrer_diccionario_minmay,
                self.recorrer_diccionario_transpuesto,
                self.recorrer_diccionario_complementos,
                self.recorrer_diccionario_intercalado,
            ]:
                metodo, resultado = estrategia()
                if resultado is not False:
                    imprimir_resultados(metodo, resultado)

        # Si llega a la siguiente linea, no se encontro el resultado
        imprimir_resultados(metodo, resultado)


class AtaqueFuerzaBruta:
    """Implementa distintos algoritmos para obtener colisiones
    contra un hash conocido en base a secuencias
    """

    def __init__(
        self,
        hash_comprobar,
    ):
        """Ofrece métodos para comprobar un hash
            contra un diccionario

        :param hash_comprobar: El hash que se desea romper
        :param archivo_diccionario: Archivo con palabras a comprobar
        :param archivo_complementos: Archivo con prefijos y sufijos
        :param archivo_intercalado: Archvio con infijos/interfijos
        :returns: Nada

        """
        self.hash_comprobar = hash_comprobar

    def secuencia_reglas(self, caracteres, archivo_complementos=None):
        """Genera y comprueba secuencias generadas
        en base a reglas predefinidas de largo y
        conjunto de caracteres
        Si el paramaetro archivo_complementos tiene un valor,
        lo comprueba junto con la secuencia
        """

        l_min = input("Longitud mínima de la cadena: ")
        l_max = input("Longitud máxima de la cadena: ")

        for longitud in range(int(l_min), int(l_max) + 1):
            productos = itertools.product(caracteres, repeat=longitud)
            for palabra in productos:
                if archivo_complementos is not None:
                    for comp in obtener_lineas(archivo_complementos):
                        palabra = "".join(palabra)
                        palabra_prefijo = comp + palabra
                        palabra_sufijo = palabra + comp
                        sha1_hash_pre = sha1(palabra_prefijo.encode())
                        sha1_hash_suf = sha1(palabra_sufijo.encode())
                        if sha1_hash_suf.hexdigest() == self.hash_comprobar:
                            return "Furza bruta con complementos", palabra_sufijo
                        if sha1_hash_pre.hexdigest() == self.hash_comprobar:
                            return "Fuerza bruta con complementos", palabra_prefijo
                else:
                    palabra = "".join(palabra)
                    sha1_hash = sha1(palabra.encode())

                    if sha1_hash.hexdigest() == self.hash_comprobar:
                        return "Fuerza bruta secuencial", palabra
        return "Fuerza bruta", False

    def menu_clase(self):
        """Imprime un menu para el usuario"""

        ataque = 0
        while ataque < 1 or ataque > 2:
            print(
                """
                FUERZA BRUTA\n
                Seleccione el ataque
                ================================
                1 - Solo fuerza bruta
                2 - Fuerza bruta mas prefijos
                ================================
                """
            )
            ataque = int(input("Opción: "))
        opcion = 0
        while opcion < 1 or opcion > 6:
            print(
                """
                FUERZA BRUTA\n
                Seleccione el conjunto de pruebas
                ================================
                1 - ascii minúsculas
                2 - ascii mayúsculas
                3 - ascii minúsculas y mayúsculas
                4 - numeros
                5 - ascii y numeros
                6 - todas las anteriores y símbolos
                ================================
                """
            )
            opcion = int(input("Opción: "))
        if opcion == 1:
            caracteres = string.ascii_lowercase
        elif opcion == 2:
            caracteres = string.ascii_uppercase
        elif opcion == 3:
            caracteres = string.ascii_letters
        elif opcion == 4:
            caracteres = string.digits
        elif opcion == 5:
            caracteres = string.ascii_letters + string.digits
        elif opcion == 6:
            caracteres = string.printable

        if ataque == 2:
            archivo_complementos = input(
                "Indique el nombre del archivo de complementos: "
            )
            metodo, resultado = self.secuencia_reglas(caracteres, archivo_complementos)
        else:
            metodo, resultado = self.secuencia_reglas(caracteres)

        imprimir_resultados(metodo, resultado)


if __name__ == "__main__":
    # recorrer_diccionario_full()
    # corresponde a 'python123' en SHA1
    test_hash = "1854a7d8c2651e57acc7771b6644dfbf46b8ec98"
    # corresponde a 'abc2' en SHA1 para pruebas de fza bruta
    test_hash_simple = "229d028063a11904f846c91224abaa99113f3a15"
    test_dict = "diccionario.txt"
    test_complementos = "complementos.txt"
    test_intercalado = "intercalado.txt"

    ad = AtaqueDiccionario(test_hash, test_dict, test_complementos, test_intercalado)
    ft = AtaqueFuerzaBruta(test_hash_simple)

    # descomentar alguno de los siguientes para probar
    # ad.recorrer_diccionario_full()
    ft.menu_clase()
