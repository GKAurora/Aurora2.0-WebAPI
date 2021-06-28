# -*- coding: utf-8 -*-
'''
    :file: get_sites.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/23 22:18:43
'''
from pkg.crawlers.setting import HOST
from pkg.exceptions.token import TokenExpireException
from pkg.crawlers.base import BaseCrawler
import requests

class GetSites(BaseCrawler):

    @staticmethod
    def get_data(site_id:str='/'):
        try:
            url = '/rest/uninetwork-res/v1/position/subtree'
            params = {'id': f'{site_id}'}
            res = BaseCrawler.fetch(url=url, params=params)
            return res.json().get('data')
        except TokenExpireException as tke:
            res = BaseCrawler.loop_token(GetSites.get_data)
            return res