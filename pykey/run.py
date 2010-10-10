# -*- coding: utf-8 -*-
from optparse import OptionParser

import pykey.config as config

from pykey.server import Server

parser = OptionParser()
parser.add_option("-p", "--port", type="int", default=config.conf["port"],
                   help="host to listen [%default]")
parser.add_option("-H", "--host", default=config.conf["host"],
                   help="host to listen [%default]")

option, args = parser.parse_args()

def main():
    sv = Server(option.host, option.port)
    sock = sv.get_sock()
    while True:
        conn, addr = sock.accept()

if __name__ == "__main__":
    main()
