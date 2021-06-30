# -*- coding: utf-8 -*-
'''
    :file: sysMessage.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/30 12:33:09
'''

import time
import psutil

# print(time.time())
# data = psutil.cpu_percent(interval=1)
# print(data)
# print(psutil.cpu_percent(interval=1, percpu=True))
# # print(len(data))
# print(time.time())

import html

s = '&#x7b;9c-50-ee-1d-f2-6b&#x3d;-55&#x7d;'
print(html.unescape(s))