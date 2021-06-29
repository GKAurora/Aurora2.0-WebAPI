# -*- coding: utf-8 -*-
'''
    :file: sdn_info.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/17 20:30:49
'''

from pkg.schemas.sdn import GetSpeedInSchema, UserListInSchema, UserRouteInSchema
from pkg.crawlers.users.get_users import GetUserInfoCrawler
from pkg.crawlers.users.get_sites import GetSites
import re
from apiflask import APIBlueprint, input, output, abort
from apiflask.decorators import auth_required, doc
from flask.views import MethodView
from flask.globals import current_app, request
# 
from pkg.extensions import auth
from pkg.schemas import make_res
# crawlers
from pkg.crawlers.users.heatmap import HeatMap
from pkg.crawlers.system.speeds import BaseSpeed
from pkg.crawlers.users.get_users import GetUserInfoCrawler
from pkg.crawlers.users.get_err import GetUserErrCrawler

sdn_bp = APIBlueprint('sdn', __name__)


@sdn_bp.route('/get_sdn_info')
class SDNBaseInfoView(MethodView):

    @auth_required(auth)
    @doc(summary='获取站点信息', description='传入query string-> site_id，返回对应站点信息，默认返回所有站点')
    def get(self):
        site_id = request.args.get('site_id', '/')
        sites = GetSites.get_data(site_id=site_id)
        return make_res(data=sites)
    
    @auth_required(auth)
    @doc(summary='质量评估体系健康度趋势',
        description='返回总速率，健康度，成功率，漫游达标率等各种健康度信息')
    @input(GetSpeedInSchema)
    def post(self, data):
        speeds = BaseSpeed.get_total_speed(**data)
        return make_res(data=speeds)

# sdn_base_info = SDNBaseInfoView.as_view('SDNBaseInfoView')
# sdn_bp.add_url_rule('/get_sdn_info/', defaults={"site_id": "/"}, view_func=sdn_base_info)
# sdn_bp.add_url_rule('/get_sdn_info/<site_id>', view_func=sdn_base_info)

@sdn_bp.route('/heatmap')
class HeatMapView(MethodView):

    @auth_required(auth)
    @doc(description="获取各个ap节点接入数量")
    def get(self):
        """热力图接口

        Returns:
            json: 标准响应体
        """
        res = HeatMap.get_data()
        return make_res(data=res)


@sdn_bp.route('/get_user_route')
class GetUserRouteView(MethodView):
    """用户路径接口
    """

    @auth_required(auth)
    @input(UserListInSchema)
    def put(self, data):
        """获取用户列表
        """
        res = GetUserInfoCrawler.get_data(**data)
        return make_res(data=res)



    @auth_required(auth)
    @doc(summary='获取用户路径', description='获取用户一周内的移动路径')
    @input(UserRouteInSchema)
    def post(self, data):
        res = GetUserInfoCrawler.get_user_route(**data)
        return make_res(data=res)

    
@sdn_bp.route('/get_err')
class GetErrorView(MethodView):

    @doc(summary="查询用户接入失败数据")
    # @input()
    def post(self, data):
        res = GetUserErrCrawler.get_data(**data)
        return make_res(data=res)




# @sdn_bp.route("/getUserInfo")
# # @auth_required(auth)
# class GetUserInfoView(MethodView):
    
#     @auth_required(auth)
#     @doc(description="获取接入用户信息")
#     def get(self):
#         return make_res(data={
#                 "userMac": "97-ff-d2-49-7f-bd",
#                 "userName": "97ffd2497fbd",
#                 "vipType": 0,
#                 "accessType": 1,
#                 "lastJoinRes": 2,
#                 "totalTimes": 4469,
#                 "worseTimes": 0,
#                 "joinFailTimes": 0,
#                 "rssiAvg": -23,
#                 "rateAvg": 2022,
#                 "snrAvg": 0,
#                 "totalBytes": 15965,
#                 "joinTotalTimes": 15,
#                 "joinCostTimeAvg": 0,
#                 "userType": None,
#                 "dualFrequency": None,
#                 "vendor": "HUAWEI TECHNOLOGIES CO.,LTD",
#                 "apName": None,
#                 "apMac": None,
#                 "band": None,
#                 "accTime": 1623913241299,
#                 "vipflag": None,
#                 "latency": 25,
#                 "packetloss": 2,
#                 "totalPoorTimes": 0,
#                 "minAccTime": 1623898804240,
#                 "roamingSuccTimes": 0,
#                 "roamingTotalTimes": 0,
#                 "linkQuality": 0.4525382378228473
#             })
    