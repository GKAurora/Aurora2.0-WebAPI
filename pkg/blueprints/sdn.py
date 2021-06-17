# -*- coding: utf-8 -*-
'''
    :file: sdn_info.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/17 20:30:49
'''

from apiflask import APIBlueprint, input, output, abort
from apiflask.decorators import auth_required, doc
from flask.views import MethodView
# 
from pkg.extensions import auth
from pkg.schemas import make_res

sdn_bp = APIBlueprint('sdn', __name__)

@sdn_bp.route("/getSdnInfo")
class SDNBaseInfoView(MethodView):

    @auth_required(auth)
    @doc(description='获取系统基本信息')
    def get(self):
        data = {
            'deviceInfo': [{
                "id": 1,
                "status": 6,
                "mac": "SD-SD-SD-SD-SD"
            },{
                "id": 1,
                "status": 6,
                "mac": "SD-SD-SD-SD-SD"
            },{
                "id": 1,
                "status": 6,
                "mac": "SD-SD-SD-SD-SD"
            },{
                "id": 1,
                "status": 6,
                "mac": "SD-SD-SD-SD-SD"
            }]
        }
        return make_res(data=data)


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
    