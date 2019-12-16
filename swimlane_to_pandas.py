from swimlane import Swimlane
import pandas
from io import StringIO

swimlane_url = ''
user=''
password=''
app_id=''
report_id=''

swimlane = Swimlane(swimlane_url, user, password, verify_ssl=False)

report = swimlane.request('get', '/reports/{}'.format(report_id)).json()
response = swimlane.request('post', 'search/export', json=report)
csv = StringIO(response.text)

panda_data = pandas.read_csv(csv)

print(panda_data)
