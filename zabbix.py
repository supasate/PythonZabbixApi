import requests

class ZabbixError(Exception):
    pass

class Api(object):
    def __init__(self, server='http://localhost/zabbix'):
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })
        self.url = server + '/api_jsonrpc.php'
        self.auth = ''
        self.id = 0

    def login(self, user='', password=''):
        json_response = self.do_request('user.login', {'user': user, 'password': password})
        self.auth = json_response['result']
        print 'Log in successful. Welcome %s.' % (user)

    def logout(self):
        json_response = self.do_request('user.logout')
        if (json_response['result'] == True):
            print 'Logged out. Good bye'
        else:
            print 'Log out failed. You might already log out.'

    def do_request(self, method, params=None):
        json_payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or {},
            'auth': self.auth,
            'id': self.id,
        }
        self.id += 1
        response = self.session.post(self.url, data = json.dumps(json_payload))

        if response.status_code != 200:
            raise ZabbixError("HTTP ERROR %S: %S" % (response.status, response.reason))
        if response.text == '':
            raise ZabbixError("Received empty response")

        return response.json()

