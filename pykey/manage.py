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
    queries = pykey.memory.Query()
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
            elif cmd.strip() == "sav!":
                self.queries.save()
                self.keys.last = self.keys.check_last()
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
                    self.keys.increase_last()
                    for k in self.store.data:
                        self.keys.add(k, self.keys.last)
                    self.store.reset()
                if self.queries.count >= pykey.config.conf["query_size"]:
                    self.queries.save()
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
                except EOFError:
                    break
    def read_all_binary_from(self, point):
        with open(pykey.config.conf["file"], "rb") as f:
            f.seek(pykey.config.conf["page"] * point)
            data = f.read()
        return data

    def read_at(self, point):
        with open(pykey.config.conf["file"], "rb") as f:
            f.seek(point * pykey.config.conf["page"])
            return self.binary_to_object(f.read(pykey.config.conf["page"]))

    def read_binary_at(self, point):
         with open(pykey.config.conf["file"], "rb") as f:
            f.seek(point * pykey.config.conf["page"])
            return f.read(pykey.config.conf["page"])

    def read_all_data(self):
        with open(pykey.config.conf["file"], "rb") as f:
            i = 0 
            while True:
                try:
                    f.seek(i * pykey.config.conf["page"])
                    d = self.binary_to_object(f.read(pykey.config.conf["page"]))
                    for k, d in d.items():
                        yield k, d
                    i = i + 1
                except EOFError:
                    break

    def write(self, data):
        with open(pykey.config.conf["file"], "ab") as f:
            f.write(self.fill(self.object_to_binary(data)))

    def write_at(self, data, point):
        buf = StringIO()
        for p in xrange(0, point):
            buf.write(self.read_binary_at(p))
        buf.write(self.fill(self.object_to_binary(data)))
        buf.write(self.read_all_binary_from(point + 1))
        adjust = buf.getvalue()
        buf.close()
        with open(pykey.config.conf["file"], "w") as f:
            f.write(adjust)

    def binary_to_object(self, binary):
        try:
            return marshal.loads(binary)
        except ValueError:
            return ''

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

    def initialize_file(self, name):
        with open(name, "wb") as f:
            f.write(self.fill(struct.pack("h", 0)))
