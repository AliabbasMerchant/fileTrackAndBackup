#!/usr/bin/env python3
def ret() -> (str, str):
    return None, 'a'


print(ret())


import subprocess


def execute_bash(command: str) -> (str, str):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if not output is None:
        output = output.decode('ascii')
    if not error is None:
        error = error.decode('ascii')
    return output, error
    
a = execute_bash('mkdir A')
b = execute_bash('mkdir A')
print('done')


import time
# print(time.time())
# from datetime import timezone, datetime
# print(datetime.now(tz=timezone.utc).timestamp())

import datetime
# st = datetime.datetime.fromtimestamp(1533381850)
st = datetime.datetime.fromtimestamp(time.time())
print(st)

import os
print(os.stat('test/B/test.txt'))
with open('test/B/test.txt', 'r') as f:
    print(f.read())
print(os.stat('test/B/test.txt'))

# st_atime=1533381335, st_mtime=1533381330, st_ctime=1533381330
# st_atime=1533381335, st_mtime=1533381330, st_ctime=1533381330
# st_atime=1533381335, st_mtime=1533381330, st_ctime=1533381330