import sys
sys.path.append('../')

import zabbix

config = {}
execfile("config.py", config)

server = config["server"]
username = config["user"]
password = config["password"]

api = zabbix.Api(server)
api.login(username, password)
print api.get_hostgroup()
api.logout()
