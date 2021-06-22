from requests.api import head


# -*- coding: utf-8 -*-
'''
    :file: RequestError.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/22 16:43:04
'''

class RequestException(Exception):
    def __str__(self) -> str:
        return repr('请求出错')