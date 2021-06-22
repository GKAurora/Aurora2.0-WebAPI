# -*- coding: utf-8 -*-
'''
    :file: base.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/22 16:14:38
'''
import json
from pkg.crawlers.setting import HOST, INITVAL_CODE, TIMEOUT
from pkg.exceptions.reqerror import RequestException
from fake_headers import Headers
import requests

class BaseCrawler(object):
    
    def __init__(self, token=None) -> None:
        self.token = token

    @staticmethod
    def generate_header(**kwargs):
        token = kwargs.get('token', None)
        headers = Headers(headers=True).generate()
        headers.setdefault('Content-Type', 'application/json')
        if token != None:
            headers.setdefault('X-Auth-Token', token)
        kwargs.setdefault('headers', headers)
        kwargs.setdefault('timeout', TIMEOUT)
        return kwargs

    @staticmethod
    def fetch(url:str, **kwargs):
        url = f'{HOST}{url}'
        try:
            kwargs = BaseCrawler.generate_header(**kwargs)
            response = requests.get(url, **kwargs)
            if response.status_code in INITVAL_CODE:
                response.encoding = 'utf-8'
                return response
        except requests.ConnectionError:
            return 
    
    @staticmethod
    def post(url:str, **kwargs):
        url = f'{HOST}{url}'
        try:
            kwargs = BaseCrawler.generate_header(**kwargs)
            kwargs.setdefault('verify', False)
            req_data = kwargs.get('data', None)
            if req_data:
                data = json.dumps(req_data)
            kwargs.pop('data')
            response = requests.post(url, data=data, **kwargs)
            print(response)
            if response.status_code in INITVAL_CODE:
                response.encoding = 'utf-8'
                return response
            raise RequestException
        except requests.ConnectionError:
            print("链接错误")

    @staticmethod
    def put(url:str, **kwargs):
        url = f'{HOST}{url}'
        try:
            kwargs = BaseCrawler.generate_header(**kwargs)
            kwargs.setdefault('verify', False)
            req_data = kwargs.get('data', None)
            if req_data:
                data = json.dumps(req_data)
            kwargs.pop('data')
            response = requests.put(url, data=data, **kwargs)
            if response.status_code in INITVAL_CODE:
                response.encoding = 'utf-8'
                return response
            raise RequestException
        except requests.ConnectionError:
            print("链接错误")