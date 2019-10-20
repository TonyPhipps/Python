import os
import csv
from process import Process

pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
processes = [Process(pid).__dict__ for pid in pids]

keys = processes[0].keys()

with open('processes.csv', 'w') as output_csv:
    dw = csv.DictWriter(output_csv, keys)
    dw.writeheader()
    dw.writerows(processes)

# for process in processes:
#     print(process)