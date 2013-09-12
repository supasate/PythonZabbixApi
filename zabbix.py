import requests
import json

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

    def get_hostgroup(self, output='extend', sortfield='name'):
        """ output = 'extend'|'shorten'|'refer'|list of fields
              - 'extend' = get all info [default]
              - 'shorten' = get only ids an object
              - 'refer' = get id of an object and also ids of related objects
              - list of fields, like ['groupid', 'name'] = get only listed fields
        """
        json_response = self.do_request('hostgroup.get', {'output': output, 'sortfield': sortfield})
        return json_response['result']

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

