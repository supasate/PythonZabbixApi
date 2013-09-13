import sys
sys.path.append('../')

import zabbix
from datetime import datetime
from datetime import timedelta
from calendar import timegm

# read config file
config = {}
execfile("config.py", config)

# new api instance
server = config["server"]
api = zabbix.Api(server)

# log in
username = config["user"]
password = config["password"]
api.login(username, password)

# get history
# host id
http_host_id = config["http_host_id"]
# item id
http_processor_time = config["http_processor_time_id"]
# start time and end time
time_from = timegm((datetime.now() - timedelta(minutes = 100)).utctimetuple()) - 150000
time_till = timegm(datetime.now().utctimetuple()) - 150000
print api.get_history('float', http_host_id, http_processor_time, time_from, time_till)

# log out
api.logout()
