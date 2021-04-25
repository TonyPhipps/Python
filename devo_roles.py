# Filename: devo_roles.py
# Anthony Phipps
# Copyright: GPLv3
# Description: Export and Import (provision) Devo Roles
# Example: -k "aaa" -s "bbb" -d "domain@company" --export "export.json"
# Example: -k "aaa" -s "bbb" -d "domain@company" --provision "export.json"

import argparse
import csv
import json
import datetime
import time
import hmac
import hashlib
import requests

class DevoApi:
    '''
        Devo API connection.
    '''

    def __init__(self, api_key, api_secret, domain):
        self.api_key = api_key
        self.api_secret = api_secret
        self.domain = domain

        self.api_url_base = 'https://api-us.devo.com/probio/domain/{}'.format(self.domain)
        
        timestamp = str(int(time.time()) * 1000)

        sign = hmac.new(self.api_secret.encode(), (self.api_key + timestamp).encode(), hashlib.sha256).hexdigest()

        self.headers = {
            'x-logtrust-domain-apikey': api_key,
            'x-logtrust-sign': sign,
            'x-logtrust-timestamp': timestamp,
            'Content-Type': "application/json",
            }

    def get_headers(self):
        return self.headers
    
    def get_api_url_base(self):
        return self.api_url_base

def get_roles(api_url_base, headers):
    api_url = '{}/roles'.format(api_url_base)
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        json_data = json.loads(response.text)
        return json_data

    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None

def get_role(api_url_base, headers, role, full='false'):
    api_url = '{}/roles/{}?full={}'.format(api_url_base, role, full)
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        json_data = json.loads(response.text)
        return json_data

    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None

def put_role(api_url_base, headers, data):
    api_url = '{}/roles/'.format(api_url_base)

    print('url: {}'.format(api_url))
    print('headers: {}'.format(headers))
    print('data: {}'.format(data))

    response = requests.post(api_url, headers=headers, data=data)
    
    if response.status_code == 200:
        return True

    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', default=None, help='Specify the API Key.')
    parser.add_argument('-s', '--secret', default=None, help='Specify the API Secret.')
    parser.add_argument('-d', '--domain', default=None, help='Specify the Devo Domain.')

    parser.add_argument('-e', '--export', default=None, help='Export to json file.')
    parser.add_argument('-p', '--provision', default=None, help='Import from json file.')
    args = parser.parse_args()

    connection = DevoApi(args.key, args.secret, args.domain)

    roles = get_roles(connection.get_api_url_base(), connection.get_headers())

    role_details = []
    for role in roles:
        role_name = role['name']
        role_details.append(
            get_role(connection.get_api_url_base(),
            connection.get_headers(),
            role_name,
            full='true')
        )

    if args.export is not None:
        export_file = args.export
        for role in role_details:
            with open(export_file, 'a') as file:
                file.write(json.dumps(role) + '\n')

    elif args.provision is not None:
        with open(args.provision) as file:
            for line in file:
                role = json.loads(line)
                response=put_role(connection.get_api_url_base(),
                    connection.get_headers(),
                    role)
                print(response)

    else:
        for role in role_details:
            print(role)

if __name__ == '__main__':
    main()
