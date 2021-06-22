# -*- coding: utf-8 -*-
'''
    :file: setting.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/22 16:15:15
'''
from environs import Env

env = Env()
env.read_env()

HOST = env.str('HOST', 'https://117.78.31.209:26335')

TIMEOUT = env.int('TIMEOUT', 30)
HUAWEI_USERNAME = env.str('HUAWEI_USERNAME', '13727494636')
HUAWEI_PASSWORD = env.str('HUAWEI_PASSWORD', "farmer123!@#")

INITVAL_CODE = env.list('INITVAL_CODE', [200, 206])