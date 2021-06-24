# -*- coding: utf-8 -*-
'''
    :file: get_oneline_users.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/24 18:23:33
'''
from typing import List
from pkg.crawlers.base import BaseCrawler
from pkg.exceptions.token import TokenExpireException
from pkg.util.stamp import *
import math

class GetUserInfoCrawler(BaseCrawler):

    @staticmethod
    def get_data(site_id, page:int=1, page_size:int=200):
        try:
            url = '/rest/campusclientservice/v1/event/userlist'
            data = {
                "regionType": "site",
                "level": "1",
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
            BaseCrawler.get_token()
            return GetUserInfoCrawler.get_data(site_id)

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
            BaseCrawler.get_token()
            # if total_size < raw_data.get('pageSize'):
                
            
            # for user in raw_data.


