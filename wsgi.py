# -*- coding: utf-8 -*-
'''
    :file: wsgi.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/07/01 17:10:05
'''

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from pkg import create_app

app = create_app('production')