import csv
import json
import requests


api_url_base = 'https://defense-prod05.conferdeploy.net/'
api_secret = ''
api_id = ''
org_id = ''
org_key = ''

headers = {'Content-Type': 'application/json',
           'User-Agent': 'Python',
           'X-Auth-Token': '{}/{}'.format(api_secret, api_id)}


def get_watchlists(org_key):
    
    api_url = '{}threathunter/watchlistmgr/v3/orgs/{}/watchlists'.format(api_url_base, org_key)

    response = requests.get(api_url, headers=headers)
    json_data = json.loads(response.text)
    results = json_data['results']

    if response.status_code == 200:
        return (results)
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None

def save_watchlists():
    result = get_watchlists(org_key)
    # print(result)
    data = open('watchlists.csv', 'w', newline="")
    
    csvwriter = csv.writer(data)
    count = 0
    for emp in result:
        if count == 0:
                header = emp.keys()
                csvwriter.writerow(header)
                count += 1
        csvwriter.writerow(emp.values())
    data.close()


def get_devices_export(org_key):
    
    status = 'PENDING, REGISTERED, UNINSTALLED, DEREGISTERED, ACTIVE, INACTIVE, ERROR, ALL, BYPASS_ON, BYPASS, QUARANTINE, SENSOR_OUTOFDATE, DELETED, LIVE'
    
    api_url = '{}appservices/v6/orgs/{}/devices/_search/download?status={}'.format(api_url_base, org_key, status)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return (response.content)
    else:
        print('[!] HTTP {0} calling [{1}]'.format(response.status_code, api_url))
        return None

def save_devices_export():

    result = get_devices_export(org_key)

    if result is not None:
        #print(result)

        with open('devices.csv', 'wb') as text_file:
            text_file.write(result)
    else:
        print('No results')

save_devices_export()
save_watchlists()
