# -*- coding: utf-8 -*-
import os

from optparse import OptionParser

import pykey.config as config

from pykey.server import Server
from pykey.manage import ClientManager
from pykey.manage import FileManager
from pykey.memory import Key

parser = OptionParser()
parser.add_option("-p", "--port", type="int", default=config.conf["port"],
                   help="host to listen [%default]")
parser.add_option("-H", "--host", default=config.conf["host"],
                   help="host to listen [%default]")

option, args = parser.parse_args()

def main():
    sv = Server(option.host, option.port)
    sock = sv.get_sock()
    file_size = os.path.getsize(config.conf["file"])
    keys = Key()
    keys.last = (file_size / config.conf["page"]) - 1
    for k, i in FileManager().read_all_keys():
        keys.add(k, i)
    while True:
        conn, addr = sock.accept()
        #TODO logging Address
        cm = ClientManager(conn)
        cm.start()

if __name__ == "__main__":
    main()
