# https://docs.devo.com/confluence/ndt/api-reference/provisioning-api/authorizing-provisioning-api-requests
# https://api-us.devo.com/probio/apiDoc/index.html

import time
import hmac
import hashlib
import requests
import json

api_key = ''
api_secret = ''
domain = ''

api_url_base = 'https://api-us.devo.com/probio/domain/{}'.format(domain)
timestamp = str(int(time.time()) * 1000)

sign = hmac.new(api_secret.encode(), (api_key + timestamp).encode(), hashlib.sha256).hexdigest()

headers = {
    'x-logtrust-domain-apikey': api_key,
    'x-logtrust-sign': sign,
    'x-logtrust-timestamp': timestamp,
    'Content-Type': "application/json",
    }

def get_roles():
    api_url = '{}/roles'.format(api_url_base)
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        json_data = json.loads(response.text)
        for obj in json_data:
            print(obj)

    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None

get_roles()
