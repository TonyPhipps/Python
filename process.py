# Filename: procees.py
# Anthony Phipps
# Copyright: GPLv3

import socket
import datetime
import os
import re

class Process:
    '''
        Parsed properties from /proc/ given a process ID (pid).
    '''
    def __init__(self, pid):
        self.host = socket.getfqdn()
        self.date_scanned = datetime.datetime.now().replace(microsecond=0).isoformat()
        self.pid = int(pid)
        self.status = (open(os.path.join('/proc', pid, 'status'), 'rb')).read().decode()
        self.cmdline = open(os.path.join('/proc', pid, 'cmdline'), 'rb').read().decode()

        # /proc/pid/status
        # Reference: http://man7.org/linux/man-pages/man5/proc.5.html
        self.name = re.search(r'Name:\s(.+)', self.status).groups()[0],
        self.state = re.search(r'State:\s(.+)', self.status).groups()[0],
        self.ppid = re.search(r'PPid:\s(.+)', self.status).groups()[0],
        self.real_uid = re.search(r'Uid:\s(.+)', self.status).groups()[0].split()[0],
        self.effective_uid = re.search(r'Uid:\s(.+)', self.status).groups()[0].split()[1],
        self.saved_uid = re.search(r'Uid:\s(.+)', self.status).groups()[0].split()[2],
        self.real_gid = re.search(r'Gid:\s(.+)', self.status).groups()[0].split()[0],
        self.effective_gid = re.search(r'Gid:\s(.+)', self.status).groups()[0].split()[1],
        self.saved_gid = re.search(r'Gid:\s(.+)', self.status).groups()[0].split()[2],
        self.threads = re.search(r'Threads:\s(.+)', self.status).groups()[0],

        #/proc/pid/cmdline
        self.cmdline = self.cmdline.split('\0')[0]

    def __str__(self):
        process = {
            "host": self.host,
            "date_scanned" : self.date_scanned,
            "pid" : self.pid,

            # /proc/pid/status
            # Reference: http://man7.org/linux/man-pages/man5/proc.5.html
            "name" : self.name,
            "state" : self.state,
            "ppid" : self.ppid,
            "real_uid" : self.real_uid,
            "effective_uid" : self.effective_uid,
            "saved_uid" : self.saved_uid,
            "real_gid" : self.real_gid,
            "effective_gid" : self.effective_gid,
            "saved_gid" : self.saved_gid,
            "threads" : self.threads,

            #/proc/pid/cmdline
            "cmdline" : self.cmdline
        }

        # Print Dictionary
        return process