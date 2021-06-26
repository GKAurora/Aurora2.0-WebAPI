# -*- coding: utf-8 -*-
'''
    :file: time_parse.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/26 17:59:24
'''
import datetime
from time import time


def get_utc_time(stamp:int):
    utc_time = datetime.datetime.utcfromtimestamp(stamp / 1000)
    return utc_time.strftime("%Y-%m-%dT %H:%M:%SZ")