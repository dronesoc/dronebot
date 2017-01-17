import requests
import os
import json

"""
Defines a connection to a Persist Key/Value Store
"""
class PersistStore:
    def __init__(self):
        self.base_url = 'https://beepboophq.com/api/v1/persist/kv'
        self.token = os.getenv("BEEPBOOP_TOKEN", "")

    def list_keys(self):
        r = requests.get(self.base_url, headers={'Authorization': 'Bearer {}'.format(self.token)})
        return r.json()

    def set_value(self, key, value):
        r = requests.put(self.base_url + '/{}'.format(key), headers={'Authorization': 'Bearer {}'.format(self.token)}, data=json.dumps({'value': value}))
        if r.status_code != 200:
            print r.text

    def get_value(self, key):
        r = requests.get(self.base_url + '/{}'.format(key), headers={'Authorization': 'Bearer {}'.format(self.token)})
        return r.json()['value']

