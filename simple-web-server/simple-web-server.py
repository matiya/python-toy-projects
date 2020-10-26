#!/usr/bin/env python

import os
import http.server


class case_directory:
    def test(self, handler):
        return os.path.isdir(handler.full_path)

    def act(self, handler):

        file_items = ""
        dir_items = ""
        # regresa los archivos en un directorio
        # FIXME Si pido directorio/ funciona, pero con directorio no
        # FIXME Tal vez crear otro método para ordenar esto?
        for top_dir, subdirs, files in os.walk(handler.full_path):
            for item in files:
                handler.full_path + item
                if os.path.isfile(handler.full_path + item):
                    file_items += f"<li><a href={item}>\
                                    {item}</a></li>\n"
            for subdir in subdirs:
                if os.path.isdir(handler.full_path + subdir):
                    dir_items += f"<li><a href={subdir}>\
                                    {subdir}</a></li>\n"
        index_page = f"""<html>
                        <body>
                        <h2> Archivos </h2>
                        <ul> {file_items} </ul>
                        <h2> Directorios </h2>
                        <ul> {dir_items} </ul>
                        </body>
                        </html>
                    """
        print(index_page)
        handler.send_page(content=index_page.encode())


class case_file:
    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        print("case_existing_file")
        handler.handle_file()


class case_invalid_path:
    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        print("case_invalid_path")
        handler.send_page(status=404)


class case_error:
    def test(self, handler):
        return True

    def act(self, handler):
        print("case_error")
        handler.handle_error(f"{handler.path} no encontrado")


class RequestHandler(http.server.BaseHTTPRequestHandler):
    """Regreso una página básica"""

    template = """\
               <html>
               <body>
                   <h2> {msg} </h2>
               <table>
               <tr>  <td>Header</td>         <td>Value</td>          </tr>
               <tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
               <tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
               <tr>  <td>Client port</td>    <td>{client_port}s</td> </tr>
               <tr>  <td>Command</td>        <td>{command}</td>      </tr>
               <tr>  <td>Path</td>           <td>{path}</td>         </tr>
               </table>
               </body>
               </html>
               """
    msg_ok = '<b style="color:green">Servidor funcionado </b>'
    msg_error = '<b style="color:red"> Objeto no encontrado </b>'
    full_path = ""

    Cases = [case_directory, case_file, case_invalid_path, case_error]

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path
            # iterar por cada caso, comprobar si aplica
            # y  ejecutar una accion de ser así
            print(f"{self.full_path=}")
            for case in self.Cases:
                # instancio la clase case
                handler = case()
                if handler.test(self):
                    handler.act(self)
                    break

        except Exception as msg:
            self.handle_error(msg)

    def handle_file(self):
        try:
            html_file = open(self.full_path, "r")
            content = html_file.read()
            html_file.close()
            self.send_page(content.encode())
        except Exception as msg:
            self.handle_error(msg)

    def create_page(self, status):
        values = {
            "date_time": self.date_time_string(),
            "client_host": self.client_address[0],
            "client_port": self.client_address[1],
            "command": self.command,
            "path": self.path,
            "msg": (self.msg_ok if status == 200 else self.msg_error),
        }
        page = self.template.format(**values)
        print(page)
        return page

    def send_page(self, content=None, status=200):
        if content is None:
            content = self.create_page(status).encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(content)

    def handle_error(self, msg):
        print(f">>> Error:  {msg}")
        self.send_page(None, 404)


if __name__ == "__main__":
    serverAddress = ("", 8080)
    server = http.server.HTTPServer(serverAddress, RequestHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.shutdown()
