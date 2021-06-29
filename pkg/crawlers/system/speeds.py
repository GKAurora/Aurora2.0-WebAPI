# -*- coding: utf-8 -*-
'''
    :file: speeds.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/24 22:02:22
'''
from urllib.parse import urlencode, quote
from pkg.exceptions.token import TokenExpireException
from pkg.util.stamp import get_end_stamp, get_start_stamp
from pkg.crawlers.base import BaseCrawler


class BaseSpeed(BaseCrawler):

    @staticmethod
    def get_total_speed(
            site_id: str = "857b706e-67d9-49c0-b3cd-4bd1e6963c07",
            start_time: int = get_start_stamp(),
            end_time: int = get_end_stamp(),
            level: int = 0):
        url = '/rest/campuswlanqualityservice/v1/expmonitor/rate/basictable'
        try:
            # '%7B%22regionType%22:%22site%22,%22level%22:%220%22,%22tenantId%22:%22default-organization-id%22,%22startTime%22:%221597766400000%22,%22id%22:%22857b706e-67d9-49c0-b3cd-4bd1e6963c07%22,%22endTime%22:%221597816800000%22%7D'
            params = {
                "param": quote(str({
                    "regionType": "site",
                    "level": f"{level}",
                    "tenantId": "default-organization-id",
                    "startTime": f"{start_time}",
                    "id": f"{site_id}",
                    "endTime": f"{end_time}"
                }))
            }
            res = BaseCrawler.fetch(url=url, params=params)
            return res.json().get('data')
        except TokenExpireException as tke:
            print('tke', tke)
            res = BaseCrawler.loop_token(
                BaseSpeed.get_total_speed, site_id=site_id, start_time=start_time, end_time=end_time)
            return res
