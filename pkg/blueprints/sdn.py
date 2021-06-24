# -*- coding: utf-8 -*-
'''
    :file: sdn_info.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/17 20:30:49
'''

from pkg.crawlers.users.get_users import GetUserInfoCrawler
from pkg.crawlers.users.get_sites import GetSites
import re
from apiflask import APIBlueprint, input, output, abort
from apiflask.decorators import auth_required, doc
from flask.views import MethodView
from flask.globals import current_app
# 
from pkg.extensions import auth
from pkg.schemas import make_res
# crawlers
from pkg.crawlers.users.heatmap import HeatMap
from pkg.crawlers.system.speeds import BaseSpeed

sdn_bp = APIBlueprint('sdn', __name__)

@sdn_bp.route("/getSdnInfo")
class SDNBaseInfoView(MethodView):

    @auth_required(auth)
    @doc(description='获取站点信息')
    def get(self):
        sites = GetSites().get_data()
        for s in sites:
            s['name'] = current_app.config.get('SITES_NAME').get(s['name'])
        return make_res(data=sites)
    
    @auth_required(auth)
    @doc(description='查询用户列表')
    def post(self):
        site_id = '857b706e-67d9-49c0-b3cd-4bd1e6963c07'
        onlines = GetUserInfoCrawler.get_onlie_user_data(site_id=site_id)

        return make_res(data={
            'len': len(onlines),
            'users': onlines
        })

@sdn_bp.route('/getSpeed')
class SDNSpeedInfoView(MethodView):

    def get(self):
        speeds = BaseSpeed.get_total_speed()
        return make_res(data=speeds)

@sdn_bp.route("/getUserInfo")
# @auth_required(auth)
class GetUserInfoView(MethodView):
    
    @auth_required(auth)
    @doc(description="获取接入用户信息")
    def get(self):
        return make_res(data={
                "userMac": "97-ff-d2-49-7f-bd",
                "userName": "97ffd2497fbd",
                "vipType": 0,
                "accessType": 1,
                "lastJoinRes": 2,
                "totalTimes": 4469,
                "worseTimes": 0,
                "joinFailTimes": 0,
                "rssiAvg": -23,
                "rateAvg": 2022,
                "snrAvg": 0,
                "totalBytes": 15965,
                "joinTotalTimes": 15,
                "joinCostTimeAvg": 0,
                "userType": None,
                "dualFrequency": None,
                "vendor": "HUAWEI TECHNOLOGIES CO.,LTD",
                "apName": None,
                "apMac": None,
                "band": None,
                "accTime": 1623913241299,
                "vipflag": None,
                "latency": 25,
                "packetloss": 2,
                "totalPoorTimes": 0,
                "minAccTime": 1623898804240,
                "roamingSuccTimes": 0,
                "roamingTotalTimes": 0,
                "linkQuality": 0.4525382378228473
            })
    

@sdn_bp.route('/heatmap')
class HeatMapView(MethodView):

    @auth_required(auth)
    @doc(description="获取各个ap节点接入数量")
    def get(self):
        res = HeatMap.get_data()
        return make_res(data=res)