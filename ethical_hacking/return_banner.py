#!/usr/bin/env python3

import socket
from termcolor import colored


def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(1)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        banner = sock.recv(1024)
        return banner
    except:
        print(colored(f"[-] Could not retrieve banner for {ip,port}", "red"))
        return None


def main():
    port = 26
    ip = "192.168.1.98"

    banner = retBanner(ip, port)

    if banner:
        print(colored(f"[+] {ip} : {banner}", "green"))


if __name__ == "__main__":
    main()
