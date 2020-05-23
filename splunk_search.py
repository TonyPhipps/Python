import urllib.request, urllib.parse, urllib.error
import httplib2
from xml.dom import minidom

baseurl = ''
userName = ''
password = ''

# Set up search query
searchQuery = 'index=notable earliest=-5m@s'
searchQuery = searchQuery.strip()
# If the query doesn't already start with the 'search' operator or another
# generating command (e.g. "| inputcsv"), then prepend "search " to it.
if not (searchQuery.startswith('search') or searchQuery.startswith("|")):
    searchQuery = 'search ' + searchQuery
print(searchQuery)

# Authenticate with server.
# Disable SSL cert validation. Splunk certs are self-signed.
serverContent = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/auth/login',
    'POST', headers={}, body=urllib.parse.urlencode({'username':userName, 'password':password}))[1]
#print(serverContent)
sessionKey = minidom.parseString(serverContent).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue
print(sessionKey)

# Run the search and get the search ID.
# Disable SSL cert validation. Splunk certs are self-signed.
searchResponse = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/search/jobs','POST',
    headers={'Authorization': 'Splunk {}'.format(sessionKey)}, body=urllib.parse.urlencode({'search': searchQuery}))[1]
#print(searchResponse)

#sid = '1590206372.1283459'
sid = None
if not sid:
    sid = minidom.parseString(searchResponse).getElementsByTagName('sid')[0].childNodes[0].nodeValue
print(sid)

#searchStatus = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/search/jobs/' + sid,'GET',
#    headers={'Authorization': 'Splunk {}'.format(sessionKey)},body=urllib.parse.urlencode({}))[1]
#print(searchStatus)

searchResults = httplib2.Http(disable_ssl_certificate_validation=True).request(baseurl + '/services/search/jobs/' + sid + '/events','GET',
    headers={'Authorization': 'Splunk {}'.format(sessionKey)},body=urllib.parse.urlencode({'output_mode': 'json'}))[1]

if searchResults != b'{"preview":true,"init_offset":0,"post_process_count":0,"messages":[],"results":[]}':
    print(searchResults)

# References
# https://docs.splunk.com/Documentation/Splunk/8.0.3/RESTREF/RESTsearch
# https://docs.splunk.com/Documentation/Splunk/8.0.3/RESTTUT/RESTsearches
# https://www.splunk.com/pdfs/solution-guides/splunk-quick-reference-guide.pdf