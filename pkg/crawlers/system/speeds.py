# -*- coding: utf-8 -*-
'''
    :file: speeds.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/24 22:02:22
'''
import json
from urllib.parse import urlencode
from pkg.exceptions.token import TokenExpireException
from pkg.util.stamp import get_end_stamp, get_start_stamp
from pkg.crawlers.base import BaseCrawler


class BaseSpeed(BaseCrawler):

    @staticmethod
    def get_total_speed():
        url = '/rest/campuswlanqualityservice/v1/expmonitor/rate/basictable'
        try:
            params = urlencode(dict(param = {
                "regionType": "site",
                "level": "0",
                "tenantId": "default-organizationid",
                "startTime": f"{get_start_stamp()}",
                "id": "/",
                "endTime": f"{get_end_stamp()}"
            }))
            return params
            res = BaseCrawler.fetch(url=url, params=params)
            # print(res.json())
            return res.json()
        except TokenExpireException as tke:
            print('tke', tke)
            BaseCrawler.get_token()
            BaseSpeed.get_total_speed()
