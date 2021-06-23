# -*- coding: utf-8 -*-
'''
    :file: stamp.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/23 00:55:51
'''

from time import time, mktime, strptime

def get_stamp():
    return round(time() * 1000)

def get_end_stamp():
    return get_stamp()

def get_start_stamp():
    start_time = get_end_stamp() - (1000 * 60 * 60 * 24 * 7)
    return start_time


def make_stamp(t:str):
    """根据传入时间生成对应的时间戳

    Args:
        t (str): 栗子:'2018-01-01 10:40:30'

    Returns:
        int: 时间戳（毫秒级）
    """
    ts = int(mktime(strptime(t, "%Y-%m-%d %H:%M:%S")))
    return ts