# -*- coding: utf-8 -*-
'''
    :file: token.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/23 12:40:51
'''
class TokenExpireException(Exception):

    def __str__(self) -> str:
        return repr('华为api过期')
