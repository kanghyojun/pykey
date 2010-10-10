import pykey.manage

def set_value(key, value, store, keys):
    store[key] = value
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
    elif keys.ahs_key(key):
        #TODO:command logging
        pass
    else:
        raise Exception("{0} is nonexistent key".format(key))
    return
