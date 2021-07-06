# -*- coding: utf-8 -*-
'''
    :file: get_all.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/30 00:17:28
'''
from pkg.crawlers.base import BaseCrawler
from urllib.parse import quote
from pkg.exceptions.token import TokenExpireException
from pkg.util.stamp import get_end_stamp, get_start_stamp


class GetArgs(BaseCrawler):

    @staticmethod
    def get_data(site_id: str = "857b706e-67d9-49c0-b3cd-4bd1e6963c07",
                     start_time: int = get_start_stamp(),
                     end_time: int = get_end_stamp(),
                     level: int = 0):
        """查询质量评估体系多维度汇总数据

        Args:
            site_id (str, 站点id): [传入站点id]. Defaults to "857b706e-67d9-49c0-b3cd-4bd1e6963c07".
            start_time (int, 毫秒级): [开始时间戳]. Defaults to get_start_stamp().
            end_time (int, 毫秒级): [截至时间戳]. Defaults to get_end_stamp().
        """
        url = '/rest/campuswlanqualityservice/v1/expmonitor/overview/rate'
        try:
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

            if len(res.text) <= 5:
                return {"data": None}
            
            return res.json().get('data')
        except TokenExpireException:
            res = BaseCrawler.loop_token(GetArgs.get_data,
                                         site_id=site_id, start_time=start_time, end_time=end_time)
            return res
    
