# -*- coding: utf-8 -*-
'''
    :file: __init__.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/05/26 17:04:57
'''

def make_res(code:int=200, message:str="ok", data=None) -> dict:
    return {
        "code": code,
        "message": message,
        "data": data
    }