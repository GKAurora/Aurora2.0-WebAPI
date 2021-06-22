# -*- coding: utf-8 -*-
'''
    :file: stamp.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/23 00:55:51
'''

from time import time, mktime, strptime

def get_stamp(t:str=None):
    if t is None:
        return round(time() * 1000)
    
dt = '2018-01-01 10:40:30'
ts = int(mktime(strptime(dt, "%Y-%m-%d %H:%M:%S")))
print (ts)
