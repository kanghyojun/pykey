import pykey.func

def get_init_env():
    envs = Environment()
    envs['set!'] = pykey.func.set_value 
    envs['get'] = pykey.func.get_value 
    envs['del'] = pykey.func.del_value 
    return envs

conf = {
  "host": "127.0.0.1",
  "port": 7777,
  "notice": "pykey :: type (help) more information\n",
  "cmdline": "@> ",
  "intial_env": get_init_env()
}
