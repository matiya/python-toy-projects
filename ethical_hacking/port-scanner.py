#!/usr/bin/env python3
from socket import *
import optparse
from re import match
from termcolor import colored
from threading import Thread


def connScan(host, port):
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))
        print(colored(f"[+] Port {port}/tcp is open", "green"))
    except:
        print(colored(f"[-] Port {port}/tcp is closed", "red"))
    finally:
        sock.close()


def portScan(host, ports):
    setdefaulttimeout(1)

    for port in ports:
        t = Thread(target=connScan, args=(host, int(port)))
        t.start()


def main():
    parser = optparse.OptionParser("port-scanner.py -H <target host> -p <target ports>")
    parser.add_option("-H", dest="tgtHost", type="string", help="specify target host")
    parser.add_option(
        "-p",
        dest="tgtPorts",
        type="string",
        help="specify target port (comma separated)",
    )
    options, args = parser.parse_args()

    tgtHost = options.tgtHost
    tgtPorts = options.tgtPorts

    if not tgtHost or not tgtPorts:
        print(colored("[ERROR] Missing arguments", "red"))
        parser.print_help()
        exit()

    if not match(r"\d+\.\d+\.\d+\.\d+", tgtHost):
        print(colored("[ERROR] Target host can only be an IP Address", "red"))
        print(parser.usage)
        exit(0)

    tgtPorts = tgtPorts.split(",")

    for port in tgtPorts:
        if not match(r"\d+", port):
            print(
                colored(f"[ERROR] Target port ({port}) can only be an integer", "red")
            )
            print(parser.usage)
            exit(0)

    portScan(tgtHost, tgtPorts)


if __name__ == "__main__":
    main()
