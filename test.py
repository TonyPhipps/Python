import socket
import datetime
import os
import re

pid = '1'

status = (open(os.path.join('/proc', pid, 'status'), 'r')).read()
print(re.search(r'Name:\s(.+)', status).group(1))
print(re.search(r'State:\s(.+)', status).group(1))
print(re.search(r'PPid:\s(.+)', status).group(1))

