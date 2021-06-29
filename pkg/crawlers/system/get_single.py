# -*- coding: utf-8 -*-
'''
    :file: get_single.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/30 00:51:19
'''
from pkg.crawlers.base import BaseCrawler
from urllib.parse import quote
from pkg.exceptions.token import TokenExpireException
from pkg.util.stamp import get_end_stamp, get_start_stamp


class GetSingle(BaseCrawler):
    """获取单个维度的信息
    """
    @staticmethod
    def get_trend_data(site_id: str = "857b706e-67d9-49c0-b3cd-4bd1e6963c07",
                 start_time: int = get_start_stamp(),
                 end_time: int = get_end_stamp(),
                 level: int = 0):
        try:
            url = '/rest/campuswlanqualityservice/v1/expmonitor/common/trend'
            params = {
                "param": quote(str({
                    "id": f"{site_id}",
                    "regionType": "site",
                    "level": f"{level}",
                    "startTime": f"{start_time}",
                    "endTime": f"{end_time}",
                    "settingRefresh": False,
                    "metricType": "accessSuccessRate"}))
            }
            res = BaseCrawler.fetch(url=url, params=params)
            return res.json().get('data')
        except TokenExpireException:
            res = BaseCrawler.loop_token(GetSingle.get_trend_data,
                                         site_id=site_id, start_time=start_time, end_time=end_time)
            return res
    
    @staticmethod
    def get_data(site_id: str = "857b706e-67d9-49c0-b3cd-4bd1e6963c07",
                 start_time: int = get_start_stamp(),
                 end_time: int = get_end_stamp(),
                 level: int = 0):
        try:
            url = '/rest/campuswlanqualityservice/v1/expmonitor/common/basic'
            params = {
                "param": quote(str({
                    "id": f"{site_id}",
                    "regionType": "site",
                    "level": f"{level}",
                    "startTime": f"{start_time}",
                    "endTime": f"{end_time}",
                    "settingRefresh": False,
                    "metricType": "accessSuccessRate"}))
            }
            res = BaseCrawler.fetch(url=url, params=params)
            return res.json().get('data')
        except TokenExpireException:
            res = BaseCrawler.loop_token(GetSingle.get_data,
                                        site_id=site_id, level=level,
                                        start_time=start_time, end_time=end_time)
            return res