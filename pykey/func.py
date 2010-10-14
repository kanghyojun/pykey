import pykey.manage
import pykey.memory

def set_value(key, value, store, keys):
    if keys.has_key(key):
        pykey.memory.Cache()[key] = value
        pykey.memory.Query().add("set", key, keys[key]["point"], value)
    else:
        store[key] = value
    return

def get_value(key, store, keys):
    cache = pykey.memory.Cache()
    if store.has_key(key):
        return store[key]
    elif cache.has_key(key):
        return cache[key]
    elif keys.has_key(key):
        value = pykey.manage.FileManager().read_at(keys[key]["point"])[key]
        cache[key] = value
        return value
    else: 
        raise Exception("{0} is nonexistent key".format(key))

def del_value(key, store, keys):
    if store.has_key(key):
        pykey.memory.Query().add("del", key, None, store[key])
        del store[key]
    elif keys.has_key(key):
        value = get_value(key, store, keys)
        pykey.memory.Query().add("del", key, keys[key]["point"], value)
        del pykey.memory.Cache()[key]
        del keys[key]
    else:
        raise Exception("{0} is nonexistent key".format(key))
    return

def logging_value(types, store, keys):
    if types == "store":
        return store.__dict__ 
    elif types == "keys":
        return keys.__dict__
    elif types == "cache":
        return pykey.memory.Cache().__dict__
