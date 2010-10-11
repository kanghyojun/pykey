import pykey.func
import pykey.bendy.env

def get_init_env():
    envs = pykey.bendy.env.Environment()
    envs['set!'] = pykey.func.set_value 
    envs['get'] = pykey.func.get_value 
    envs['del'] = pykey.func.del_value 
    envs['logging'] = pykey.func.logging_value
    return envs

conf = {
  "host": "127.0.0.1",
  "port": 7777,
  "notice": "pykey :: type (help) more information\n",
  "cmdline": "@> ",
  "initial_env": get_init_env(),
  "error": "Error :: {0}\n".format,
  "get_data": "data -> {0}\n".format,
  "file": "data.st",
  "page": 50,
  "cache_size": 2,
  "query_size": 5,
}
