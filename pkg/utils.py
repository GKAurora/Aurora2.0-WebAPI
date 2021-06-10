# -*- coding: utf-8 -*-
'''
    :file: utils.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/10 18:30:10
'''

from datetime import datetime


def format_timestamp(s):
    return s * 1000

def get_timestamp():
    """获取当前时间戳

    Returns:
        timestamp: 当前的时间戳
    """
    return datetime.utcnow().timestamp() * 1000