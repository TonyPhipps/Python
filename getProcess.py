import socket
import datetime
import os
import re

def getProcess(pid):
    host = socket.getfqdn()
    date_scanned = datetime.datetime.now().replace(microsecond=0).isoformat()
    pid = str(pid)

    with open(os.path.join('/proc', pid, 'status'), 'rb') as status:
        status = status.read().decode()
        cmdline = open(os.path.join('/proc', pid, 'cmdline'), 'rb')
        cmdline = cmdline.read().decode()

        process = {
            "host": host,
            "date_scanned" : date_scanned,
            "pid" : int(pid),
            
            # /proc/pid/status
            # Reference: http://man7.org/linux/man-pages/man5/proc.5.html
            "name" : re.search(r'Name:\s(.+)', status).groups()[0],
            "state" : re.search(r'State:\s(.+)', status).groups()[0],
            "ppid" : re.search(r'PPid:\s(.+)', status).groups()[0],
            "real_uid" : re.search(r'Uid:\s(.+)', status).groups()[0].split()[0],
            "effective_uid" : re.search(r'Uid:\s(.+)', status).groups()[0].split()[1],
            "saved_uid" : re.search(r'Uid:\s(.+)', status).groups()[0].split()[2],
            "real_gid" : re.search(r'Gid:\s(.+)', status).groups()[0].split()[0],
            "effective_gid" : re.search(r'Gid:\s(.+)', status).groups()[0].split()[1],
            "saved_gid" : re.search(r'Gid:\s(.+)', status).groups()[0].split()[2],
            "threads" : re.search(r'Threads:\s(.+)', status).groups()[0],

            #/proc/pid/cmdline
            "cmdline" : cmdline.split('\0')[0]
        }

    # Print Dictionary
    for key in process:
        print(key, ':', process[key])
    print('\n') 

pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]

for pid in pids:
    getProcess(pid)
