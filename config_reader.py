"""
Config reader
"""
# import yaml


# The YAML part

# Read config
# with open("config.yaml", "r") as f:
#     config = yaml.load(f, Loader=yaml.FullLoader)
#
# print("The URS is: ", config['URL'])
# print("The user-agent is: ", config['HEADERS'])

import configparser

config_global = configparser.ConfigParser()
file = open("config.ini", "r")
config_global.read_file(file)

conf_dic = {}

for v in config_global.sections():
    k = config_global.items(v)
    print(k, v)
    conf_dic[v] = dict(k)

# print(config_global.sections())
# print(conf_dic)

print("The URS is: ", conf_dic['main']['url'])
print("The parser is: ", conf_dic['main']['parsertype'])
print("The key is: ", conf_dic['second']['key'])
