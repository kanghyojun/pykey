import threading

import pykey.config
import pykey.memory

import pykey.bendy.lexer
import pykey.bendy.parse
import pykey.bendy.evaluate

class ClientManager(threading.Thread):
    
    store = pykey.memory.Store()
    lock = threading.Lock()

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
                token = pykey.bendy.lexer.Lex().tokenize(cmd)
                parsed = pykey.bendy.parse.Parser().parse(token)
                envs = pykey.config.conf["initial_env"]
                evaluator = pykey.bendy.evaluate.evaluate
                self.lock.acquire()
                try:
                    evaled = evaluator(parsed[0], envs, self.store)
                except Exception as expt:
                    self.conn.send(pykey.config.conf["error"](expt))
                self.lock.release()
                if evaled is not None:
                    self.conn.send(pykey.config.conf["get_data"](evaled))
