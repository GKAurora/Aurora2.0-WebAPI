# -*- coding: utf-8 -*-
'''
    :file: get_floor_device.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/30 15:05:46
'''
from pkg.exceptions.token import TokenExpireException
from pkg.crawlers.base import BaseCrawler
from urllib.parse import quote

class GetFloorDevice(BaseCrawler):

    @staticmethod
    def get_data(site_id:str='540d8574-a743-4cda-a47e-3718b6a4f722',
                level:int=3):
        try:
            url = '/rest/campuswlantopowebsite/v1/wlantopo/topoinfo'
            params = {
                "param": quote(str({
                    "id": f"{site_id}",
                    "level": level,
                    "type": "floor"
                }))
            }
            res = BaseCrawler.fetch(url=url, params=params)
            return res.json().get('resultData')
        except TokenExpireException:
            res = BaseCrawler.loop_token(GetFloorDevice.get_data, site_id=site_id, level=level)
            return res