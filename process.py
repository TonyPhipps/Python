# Filename: process.py
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
        self.status = (open(os.path.join('/proc', pid, 'status'), 'r')).read()
        self.cmdline = (open(os.path.join('/proc', pid, 'cmdline'), 'r')).read()

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
        self.command = self.cmdline.replace('\0', ' ')

        del self.status
        del self.cmdline

    def __str__(self):
        return str(self.__dict__)