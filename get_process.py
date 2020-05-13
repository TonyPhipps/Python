# Filename: process.py
# Anthony Phipps
# Copyright: GPLv3

import socket
import datetime
import os
import re
import argparse
import pprint
import csv
import json

class Process:
    '''
        Parsed properties from /proc/ given a process ID (pid).
    '''
    def __init__(self, pid):
        self.host = socket.getfqdn()
        self.date_scanned = datetime.datetime.now().replace(microsecond=0).isoformat()
        self.pid = int(pid)
        self.status = (open(os.path.join('/proc', pid, 'status'), 'r')).read()
        self.cmdline_file = (open(os.path.join('/proc', pid, 'cmdline'), 'r')).read()
        self.environ_file = (open(os.path.join('/proc', pid, 'environ'), 'r')).read()

        # /proc/pid/status
        # Reference: http://man7.org/linux/man-pages/man5/proc.5.html
        self.name = re.search(r'Name:\s(.+)', self.status).group(1)
        self.state = re.search(r'State:\s(.+)', self.status).group(1)
        self.ppid = re.search(r'PPid:\s(.+)', self.status).group(1)
        self.real_uid = re.search(r'Uid:\s(.+)', self.status).group(1).split()[0]
        self.effective_uid = re.search(r'Uid:\s(.+)', self.status).group(1).split()[1]
        self.saved_uid = re.search(r'Uid:\s(.+)', self.status).group(1).split()[2]
        self.real_gid = re.search(r'Gid:\s(.+)', self.status).group(1).split()[0]
        self.effective_gid = re.search(r'Gid:\s(.+)', self.status).group(1).split()[1]
        self.saved_gid = re.search(r'Gid:\s(.+)', self.status).group(1).split()[2]
        self.threads = re.search(r'Threads:\s(.+)', self.status).group(1)

        #/proc/pid/cmdline
        self.cmdline = self.cmdline_file.replace('\0', ' ')

        #/proc/pid/environ
        self.environ = self.environ_file.replace('\0', ' ')

        del self.status
        del self.cmdline_file
        del self.environ_file

    def __str__(self):
        return str(self.__dict__)

    def toJSON(self):
        return json.dumps(self.__dict__)

    def toJSONfile(self,file):
        with open(file, 'a') as text_file:
            text_file.write(self.toJSON() + '\n')


    def toCSVFile(self, file):
            keys = self.__dict__.keys()
            values = self.__dict__.values()
            header = ', '.join(str(v) for v in keys)
            row = ', '.join(str(v) for v in values)
            csv = header + '\n' + row
            
            if os.path.isfile(file):
                with open(file, 'a') as text_file:
                    text_file.write('\n' + row)
            else:
                with open(file, 'w') as text_file:
                    text_file.write(csv)

def main():   
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pid', default=None, help='Specify a single PID to pull data from.')
    parser.add_argument('-c', '--csv', default=None, help='Export to csv file.')
    parser.add_argument('-j', '--json', default=None, help='Export to json file.')
    args = parser.parse_args()

    now = datetime.datetime.now()
    date_scanned_filename = now.strftime('%Y%m%d-%H%M%S')
    pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
    processes = [Process(pid) for pid in pids]

    if args.csv is not None:
        for process in processes:
            process.toCSVFile(args.csv)

    elif args.json is not None:
        for process in processes:
            process.toJSONfile(args.json)

    elif args.pid is not None:
        this_process = Process(args.pid).__dict__
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(this_process)
    
    else:
        for process in processes:
            print(process.toJSON())
        

if __name__ == '__main__':
    main()
