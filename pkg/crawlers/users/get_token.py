# -*- coding: utf-8 -*-
'''
    :file: get_token.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/22 16:34:13
'''
from pkg.crawlers.setting import HOST, HUAWEI_PASSWORD, HUAWEI_USERNAME
from pkg.crawlers.base import BaseCrawler
import json
import requests

class GetToken(BaseCrawler):

    @classmethod
    def get_token(cls):
        token = BaseCrawler.get_token()
        return token

