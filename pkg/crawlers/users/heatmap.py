# -*- coding: utf-8 -*-
'''
    :file: heatmap.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/23 18:06:21
'''
from pkg.crawlers.setting import MAX_DATA, MIN_DATA
from pkg.exceptions.token import TokenExpireException
from pkg.crawlers.base import BaseCrawler
from pkg.util.stamp import get_end_stamp, get_start_stamp
import math


class HeatMap(BaseCrawler):

    @staticmethod
    def get_data():
        try:
            url = f'/rest/campusrtlswebsite/v1/clientlocation/heatmap'
            params = {
                "endTime": get_end_stamp(),
                "startTime": get_start_stamp()
            }
            res = BaseCrawler.post(url=url, params=params)
            data = res.json().get('data')
            # min_data, max_data = MIN_DATA, MAX_DATA
            # for d in data:
            #     if min_data > d.get('count'):
            #         min_data = d.get('count')
            #     if max_data < d.get('count'):
            #         max_data = d.get('count')
            
            # # error = max_data - min_data
            # for d in data:
            #     d['value'] = math.floor()
            #     d.pop('count', None)
            return data
        except TokenExpireException as tke:
            print('tke', tke)
            BaseCrawler.get_token()
            return HeatMap.get_data()