import os
from process import Process

pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

for pid in pids:
    thisprocess = Process(pid)
    print(thisprocess.__str__())
