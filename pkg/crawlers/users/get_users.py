# -*- coding: utf-8 -*-
'''
    :file: get_oneline_users.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/24 18:23:33
'''
import re
from pkg.exceptions.reqerror import RequestException
from pkg.util.time_parse import get_utc_time
from typing import List
from flask.globals import current_app
from pkg.crawlers.base import BaseCrawler
from pkg.exceptions.token import TokenExpireException
from pkg.util.stamp import *
import math

class GetUserInfoCrawler(BaseCrawler):

    @staticmethod
    def get_data(site_id, page:int=1, page_size:int=200, level:int=1):
        try:
            url = '/rest/campusclientservice/v1/event/userlist'
            data = {
                "regionType": "site",
                "level": f"{level}",
                "tenantId": "default-organization-id",
                "startTime": f"{get_start_stamp()}",
                "id": f"{site_id}",
                "endTime": f"{get_end_stamp()}",
                "sortColumn": "totalcount",
                "currPage": f"{page}",
                "pageSize": f"{page_size}",
                "sortType": "desc"
            }
            response = BaseCrawler.post(url=url, data=data)
            return response.json().get('data', None)
        except TokenExpireException as tke:
            print(tke)
            if current_app.config.get('isTokenExp'):
                raise RequestException
            BaseCrawler.get_token()
            current_app.config['isTokenExp'] = True
            res = GetUserInfoCrawler.get_data(site_id, page, page_size=page_size, level=level)
            current_app.config['isTokenExp'] = False
            return res

    @staticmethod
    def get_onlie_user_data(site_id):
        try:
            raw_data:dict = GetUserInfoCrawler.get_data(site_id=site_id)
            if raw_data == None:
                return None
            table_data:List = raw_data.get('tableData')
            # 总数大于一页的数量，继续获取
            num = math.ceil(int(raw_data.get('totalSize')) / int(raw_data.get('pageSize')))
            for i in range(2, num+1):
                sec_data = GetUserInfoCrawler.get_data(site_id = site_id, page =i)
                table_data += sec_data.get('tableData')
            
            table_data = [data for data in table_data if data.get('apMac') == None]

            return table_data
        except TokenExpireException as tke:
            res = BaseCrawler.loop_token(GetUserInfoCrawler.get_onlie_user_data, site_id=site_id)
            return res


    @staticmethod
    def get_user_route(user_mac, level:int=0, site_id:str='/'):
        """获取感染者路径(获取用户接入信息)

        Args:
            user_mac (str): 用户mac地址
        """
        try:
            url = '/rest/campusclientservice/v1/protocoltrace/sessionlist'
            data = {
                "intervals": f"[\"{get_utc_time(get_start_stamp())}/{get_utc_time(get_end_stamp())}\"]",
                "level": f"{level}",
                "tenantId": "default-organization-id",
                "id": f"{site_id}",
                "accType": "1",
                "usermac": f"{user_mac}"
            }
            response = BaseCrawler.post(url=url, data=data)
            print(response)
            return response.json().get('resultData')
        except TokenExpireException as tke:
            print(tke)
            if current_app.config.get('isTokenExp'):
                raise RequestException
            BaseCrawler.get_token()
            current_app.config['isTokenExp'] = True
            res = GetUserInfoCrawler.get_user_route(user_mac=user_mac)
            current_app.config['isTokenExp'] = False
            return res

            


