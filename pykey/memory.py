import random

import pykey.manage
import pykey.func

class Store(object):

    def __new__(cls):
        if not "_the_instance" in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            cls._the_instance.data = {}
            cls._the_instance.count = 0
        return cls._the_instance

    def __setitem__(self, key, value):
        self.count = self.count + 1
        self.data[key] = value

    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key):
        self.count = self.count - 1
        del self.data[key]

    def reset(self):
        self.data = {}
        self.count = 0

    def has_key(self, key):
        return self.data.has_key(key)

class Key(object):

    last = 0

    def __new__(cls):
        if not "_the_instance" in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            cls._the_instance.data = {}
        return cls._the_instance
    
    def add(self, key, point):
        self.data[key] = {"point": point}

    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key):
        self.last = self.last - 1 if self.last > 0 else 0
        del self.data[key]

    def has_key(self, key):
        return self.data.has_key(key)

    def check_last(self):
        comp = 0
        for _, d in self.data.items():
            if comp < d["point"]:
                comp = d["point"]
        return comp

    def increase_last(self):
        self.last = self.last + 1

class Query(object):

    stack = []

    def __new__(cls):
        if not "_the_instance" in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            cls._the_instance.count = 0
        return cls._the_instance

    def add(self, types, key, point, value):
        self.count = self.count + 1
        query = {"type": types, "key": key, "point": point, "value": value}
        self.stack.append(query)
        pykey.manage.FileManager().save_query(query)

    def __getitem__(self, index):
        return self.stack[index]

    def save(self):
        fm = pykey.manage.FileManager()
        for s in self.stack:
            read_data = fm.read_at(s["point"])
            del read_data[s["key"]]
            fm.write_at(read_data, s["point"])
        self.count = 0
        self.stack = []
        fm.reset_query()

    def pop(self):
        return self.stack.pop()

    def redo(self, store, keys):
        try:
            data = self.pop()
        except IndexError:
            return
        if data["type"] == "del":
            if data["point"] is None:
                store[data["key"]] = data["value"]
            else:
                keys.add(data["key"], data["point"])
        elif data["type"] == "set":
            if store.has_key(data["key"]):
                del store[data["key"]]
            elif keys.has_key(data["key"]):
                pykey.func.del_value(data["key"], {}, keys)
                del keys[data["key"]]

class Cache(object):

    def __new__(cls):
        if not "_the_instance" in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            cls._the_instance.data = {}
            cls._the_instance.count = 0
        return cls._the_instance

    def __setitem__(self, key, value):
        self.count = self.count + 1
        if self.count >= pykey.config.conf["memcache_size"]:
            pop_size = int(pykey.config.conf["memcache_size"] * (30 / 100.0))
            pop_size = pop_size if pop_size >= 1 else 1
            for k in random.sample(self.data.keys(), pop_size):
                del self.data[k]
            self.count = self.count - pop_size
        self.data[key] = value
        
    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key):
        self.count = self.count - 1
        del self.data[key]

    def has_key(self, key):
        return self.data.has_key(key)
