# -*- coding: utf-8 -*-
'''
    :file: base.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/22 16:14:38
'''
import json
from pkg.exceptions.token import TokenExpireException
from flask import current_app
from requests.models import Response
from pkg.crawlers.setting import HOST, HUAWEI_PASSWORD, HUAWEI_USERNAME, INITVAL_CODE, TIMEOUT
from pkg.exceptions.reqerror import RequestException
from fake_headers import Headers
import requests

class BaseCrawler(object):
    
    def __init__(self, token=None) -> None:
        self.token = token

    @staticmethod
    def generate_header(**kwargs):
        token = current_app.config.get('token', None)
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
            kwargs.setdefault('verify', False)
            response = requests.get(url, **kwargs)
            print('req', response)
            if response.status_code in INITVAL_CODE:
                response.encoding = 'utf-8'
                return response
            if response.status_code == 401:
                raise TokenExpireException
            raise RequestException
        except requests.ConnectionError:
            print("链接错误")
            return 
    
    @staticmethod
    def post(url:str, **kwargs):
        url = f'{HOST}{url}'
        try:
            kwargs = BaseCrawler.generate_header(**kwargs)
            kwargs.setdefault('verify', False)
            req_data = kwargs.get('data', None)
            if req_data:
                req_data = json.dumps(req_data)
            kwargs.pop('data', None)
            response = requests.post(url, data=req_data, **kwargs)
            if response.status_code in INITVAL_CODE:
                response.encoding = 'utf-8'
                return response
            if response.status_code == 401:
                raise TokenExpireException
            raise RequestException
        except requests.ConnectionError:
            print("链接错误")
        # except Exception as e:
        #     print(type(e), e)

    @staticmethod
    def put(url:str, **kwargs) -> Response:
        """封装put方法

        Args:
            url (str): 请求接口

        Raises:
            RequestException: 请求错误

        Returns:
            [Response]: 响应体
        """
        url = f'{HOST}{url}'
        try:
            kwargs = BaseCrawler.generate_header(**kwargs)
            kwargs.setdefault('verify', False)
            req_data = kwargs.get('data', None)
            if req_data:
                req_data = json.dumps(req_data)
            kwargs.pop('data', None)
            response = requests.put(url, data=req_data, **kwargs)
            if response.status_code in INITVAL_CODE:
                response.encoding = 'utf-8'
                return response
            if response.status_code == 401:
                raise TokenExpireException
            raise RequestException
        except requests.ConnectionError:
            print("链接错误")

    @classmethod
    def get_token(cls):
        """获取华为api token

        Returns:
            str: 华为api的token
        """
        data_body = {
            "grantType": "password",
            "userName": HUAWEI_USERNAME,
            "value": HUAWEI_PASSWORD
        }
        response = BaseCrawler.put(url='/rest/plat/smapp/v1/oauth/token', data=data_body)
        token = response.json().get('accessSession')
        current_app.config.setdefault('token', token)
        return token


