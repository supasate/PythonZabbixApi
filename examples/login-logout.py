import zabbix

config = {}
execfile("config.py", config)

server = config["server"]
username = config["user"]
password = config["password"]

api = zabbix.Api(server)
api.login(username, password)
api.logout()
