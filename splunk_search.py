# Filename: splunk_search.py
# Anthony Phipps
# Copyright: GPLv3
# The sample below pulls the last 5 minutes of notable events - this could be ran every 5 minutes to establish near-realtime recording to a SIEM
# python splunksearch.py "https://yourserver.splunkcloud.com:8089" "youruser" "yourpassword" "index=notable earliest=-5m@s"

import argparse
import datetime
import httplib2
import json
import time
import urllib.request, urllib.parse, urllib.error
import pandas as pd
from xml.dom import minidom

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Provide the base URL, usually ending in :8089')
    parser.add_argument('username', help='Username')
    parser.add_argument('password', help='Password')
    parser.add_argument('search', help='Search string')
    parser.add_argument('output', help='json or csv')
    args = parser.parse_args()

    now = datetime.datetime.now()
    nowFileName = now.strftime('%Y%m%d-%H%M%S')

    baseurl = args.url
    userName = args.username
    password = args.password
    searchQuery = args.search
    output = args.output
    
    # Set up search query
    searchQuery = searchQuery.strip()
    # If the query doesn't already start with the 'search' operator or another
    # generating command (e.g. "| inputcsv"), then prepend "search " to it.
    if not (searchQuery.startswith('search') or searchQuery.startswith("|")):
        searchQuery = 'search ' + searchQuery
    #print(searchQuery)

    # Authenticate with server.
    # Disable SSL cert validation. Splunk certs are self-signed.
    serverContent = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/auth/login',
        'POST', headers={}, body=urllib.parse.urlencode({'username':userName, 'password':password}))[1]
    #print(serverContent)
    sessionKey = minidom.parseString(serverContent).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue
    #print(sessionKey)

    # Run the search and get the search ID.
    # Disable SSL cert validation. Splunk certs are self-signed.
    searchResponse = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/search/jobs','POST',
        headers={'Authorization': 'Splunk {}'.format(sessionKey)}, body=urllib.parse.urlencode({'search': searchQuery}))[1]
    #print(searchResponse)

    sid = None
    #sid = ''
    if not sid:
        sid = minidom.parseString(searchResponse).getElementsByTagName('sid')[0].childNodes[0].nodeValue
    #print(sid)

    # While loop until Splunk search has completed
    isDone = False
    while not isDone:
        searchStatus = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/search/jobs/' + sid,'GET',
            headers={'Authorization': 'Splunk {}'.format(sessionKey)},body=urllib.parse.urlencode({'output_mode': 'json'}))[1]
        searchStatus_json = json.loads(searchStatus)
        isDone = searchStatus_json['entry'][0]['content']['isDone']
        print("waiting for search to complete...")
        time.sleep(1)
        
    # Pull Search results
    searchResults = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/search/jobs/' + sid + '/events','GET',
        headers={'Authorization': 'Splunk {}'.format(sessionKey)},body=urllib.parse.urlencode({'output_mode': 'json'}))[1]
    searchResults_json = json.loads(searchResults)
    #print(searchResults_json['results'])

    # If search results contains events, dump to file
    if searchResults_json['results'] != []:
        searchResults_json = json.loads(searchResults)

        if output == "json":
            with open('splunk_' + nowFileName + '.json', 'w') as outfile:
                for result in searchResults_json['results']:
                    json.dump(result, outfile)
                    outfile.write("\n")

        if output == "csv":             
            df = pd.DataFrame(searchResults_json['results'])
            filename = 'splunk_' + nowFileName + '.csv'
            df.to_csv (filename, index=None, header=True)

if __name__ == '__main__':
    main()

# References
# https://docs.splunk.com/Documentation/Splunk/8.0.3/RESTREF/RESTsearch
# https://docs.splunk.com/Documentation/Splunk/8.0.3/RESTTUT/RESTsearches
# https://www.splunk.com/pdfs/solution-guides/splunk-quick-reference-guide.pdf