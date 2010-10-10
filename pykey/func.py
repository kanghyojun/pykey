import pykey.manage
import pykey.memory

def set_value(key, value, store, keys):
    store[key] = value
    if keys.has_key(key):
        pykey.memory.Query().add("set", key, keys[key]["point"])
    return

def get_value(key, store, keys):
    if store.has_key(key):
        return store[key]
    elif keys.has_key(key):
        return pykey.manage.FileManager().read_at(keys[key]["point"])[key]
    else: 
        raise Exception("{0} is nonexistent key".format(key))

def del_value(key, store, keys):
    if store.has_key(key):
        del store[key]
    elif keys.has_key(key):
        pykey.memory.Query().add("del", key, keys[key]["point"])
        del keys[key]
    else:
        raise Exception("{0} is nonexistent key".format(key))
    return

def logging_value(types, store, keys):
    if types == "store":
        return store.__dict__ 
    elif types == "keys":
        return keys.__dict__
    elif types == "file":
        datas = {}
        for k, d in pykey.manage.FileManager().read_all_data():
            datas[k] = d
        return datas
