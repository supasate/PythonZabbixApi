import requests

class Api(object):
    def __init__(self, server='http://localhost/zabbix'):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        self.url = server + '/api_jsonrpc.php'
        self.auth = ''
        self.id = 0

