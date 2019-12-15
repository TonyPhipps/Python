from pandas.io.json import json_normalize
from swimlane import Swimlane

swimlane_url = ''
user=''
password=''

swimlane = Swimlane(swimlane_url, user, password, verify_ssl=False)
application = swimlane.apps.get(id='')

report_data = application.reports.build('new_report', limit=0)
report_data_json = []

for record in report_data:
    json_data = record.for_json()
    report_data_json.append(json_data)

json_data_normalized = json_normalize(report_data_json)

print(json_data_normalized)
