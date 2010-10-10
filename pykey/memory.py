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

    def __new__(cls):
        if not "_the_instance" in cls.__dict__:
            cls._the_instance = object.__new__(cls)
            cls._the_instance.data = {}
            cls._the_instance.last = 0
        return cls._the_instance
    
    def add(self, key, point):
        self.data[key] = {"point": point}

    def __getitem__(self, key):
        return self.data[key]

    def has_key(self, key):
        return self.data.has_key(key)
