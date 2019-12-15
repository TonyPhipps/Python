import json
from swimlane import Swimlane

swimlane_url = ''
user=''
password=''

swimlane = Swimlane(swimlane_url, user, password, verify_ssl=False)
application = swimlane.apps.get(id='')

report_data = application.reports.build('new_report', limit=0)
report_data_json = []

with open('data.json', 'w') as outfile:
    for record in report_data:
        json_data = record.for_json()
        #print(json.dumps(json_data, indent=4))
        json.dump(json_data, outfile)

