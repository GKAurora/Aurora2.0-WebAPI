# -*- coding: utf-8 -*-
'''
    :file: get_err.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/28 13:06:50
'''
from pkg.exceptions.token import TokenExpireException
from pkg.crawlers.base import BaseCrawler
from urllib.parse import quote


class GetUserErrCrawler(BaseCrawler):

    @staticmethod
    def get_data(site_id: str = "857b706e-67d9-49c0-b3cd-4bd1e6963c07"):
        try:
            url = '/rest/campuswlanqualityservice/v1/connectivity/connect-trend'
            params = {
                "param": quote(str({
                    "accType": 1, # 0为有线用户，1为无线用户
                    "id": f"{site_id}",
                    "regionType": "site",
                    "level": 1,
                    "tenantId": "default-organization-id",
                    "startTime": 1597766400000,
                    "endTime": 1597826900000,
                    "dateFrom": 1597766400000,
                    "dateTo": 1597826900000
                }))
            }
            # params = {
            #     "param": quote('{"accType":1,"id":"/","regionType":"site","level":0,"tenantId":"default-organization-id","startTime":1597766400000,"endTime":1597826900000,"dateFrom":1597766400000,"dateTo":1597826900000}')
            # }
            res = BaseCrawler.fetch(url=url, params=params)
            return res.json().get('data')
        except TokenExpireException as tke:
            print(tke)
            res = BaseCrawler.loop_token(
                GetUserErrCrawler.get_data,
                site_id=site_id
            )
            return res
