# https://attackcti.readthedocs.io/en/latest/attackcti_overview.html

from attackcti import attack_client
import pandas

outfile = 'C:\\mitre.csv'

client = attack_client()

data = client.get_enterprise(stix_format=False)

data_panda = pandas.json_normalize(data['techniques'])

data_panda[['technique_id','technique','tactic','url']].to_csv(outfile, index=False)


