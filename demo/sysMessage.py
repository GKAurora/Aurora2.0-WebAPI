# -*- coding: utf-8 -*-
'''
    :file: sysMessage.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/30 12:33:09
'''
import time
import psutil

print(time.time())
data = psutil.cpu_percent(interval=1)
print(data)
print(psutil.cpu_percent(interval=1, percpu=True))
# print(len(data))
print(time.time())