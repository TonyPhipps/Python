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

def main():   
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', nargs='?')
    args = parser.parse_args()

    if args.pid != None:
        this_process = Process(args.pid).__dict__
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(this_process)

    else:
        pids = [pid for pid in os.listdir('/proc') if pid.isdigit()]
        processes = [Process(pid).__dict__ for pid in pids]
        keys = processes[0].keys()
        now = datetime.datetime.now()
        date_scanned_filename = now.strftime('%Y%m%d-%H%M%S')

        with open('processes_{}.csv'.format(date_scanned_filename), 'w') as output_csv:
            dw = csv.DictWriter(output_csv, keys)
            dw.writeheader()
            dw.writerows(processes)

if __name__ == '__main__':
    main()
