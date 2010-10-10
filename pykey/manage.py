import threading
import marshal
import struct

from cStringIO import StringIO

import pykey.config
import pykey.memory

import pykey.bendy.lexer
import pykey.bendy.parse
import pykey.bendy.evaluate

class ClientManager(threading.Thread):
    
    store = pykey.memory.Store()
    keys =  pykey.memory.Key()
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
                    evaled = evaluator(parsed[0], envs, self.store, self.keys)
                    if evaled is not None:
                        self.conn.send(pykey.config.conf["get_data"](evaled))
                except Exception as expt:
                    self.conn.send(pykey.config.conf["error"](expt))
                if self.store.count >= pykey.config.conf["cache_size"]:
                    FileManager().write(self.store.data)
                    self.keys.last = self.keys.last + 1
                    for k in self.store.data:
                        self.keys.add(k, self.keys.last)
                    self.store.reset()
                self.lock.release()
               
class FileManager(object):

    def read_all_keys(self):
        with open(pykey.config.conf["file"], "rb") as f:
            i = 0 
            while True:
                try:
                    f.seek(i * pykey.config.conf["page"])
                    d = self.binary_to_object(f.read(pykey.config.conf["page"]))
                    for k in d:
                        yield k, i 
                    i = i + 1
                except Exception:
                    break

    def read_at(self, point):
        with open(pykey.config.conf["file"], "rb") as f:
            f.seek(point * pykey.config.conf["page"])
            return self.binary_to_object(f.read(pykey.config.conf["page"]))
    
    def write(self, data):
        with open(pykey.config.conf["file"], "ab") as f:
            f.write(self.fill(self.object_to_binary(data)))

    def binary_to_object(self, binary):
        return marshal.loads(binary)

    def object_to_binary(self, data):
        return marshal.dumps(data)

    def fill(self, data):
        zero_hex = struct.pack("h", 0)
        length = len(data)
        space = (pykey.config.conf["page"] - length) / 2 
        buf = StringIO()
        buf.write(data)
        for x in xrange(1, space + 1):
            buf.write(zero_hex)
        if length % 2 == 1:
            buf.write(zero_hex[0])
        filled = buf.getvalue()
        buf.close()
        return filled
