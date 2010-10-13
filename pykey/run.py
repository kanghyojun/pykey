# -*- coding: utf-8 -*-
import os

from optparse import OptionParser

import pykey.config as config

import pykey.manage
import pykey.memory

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
    keys = pykey.memory.Key()
    fm = pykey.manage.FileManager()
    if os.path.isfile(config.conf["query_file"]):
        query_manager = pykey.memory.Query()
        query_manager.stack = fm.read_query()
        query_manager.save()
    if os.path.isfile(config.conf["file"]):
        file_size = os.path.getsize(config.conf["file"])
        keys.last = (file_size / config.conf["page"]) - 1
    else:
        fm.initialize_file(config.conf["file"])
        keys.last = 0
    for k, i in fm.read_all_keys():
        keys.add(k, i)
    while True:
        conn, addr = sock.accept()
        #TODO logging Address
        cm = pykey.manage.ClientManager(conn)
        cm.start()

if __name__ == "__main__":
    main()
