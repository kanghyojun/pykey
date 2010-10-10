import threading

import pykey.config

class ClientManager(threading.Thread):

    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        self.conn.send(pykey.config.conf["notice"])
        while True:
            self.conn.send(pykey.config.conf["cmdline"])
            cmd = self.conn.recv(2048)
            if cmd.strip() == '':
                pass
            else:
                # command parsing and evaluate goes here
                self.conn.send("ok")
