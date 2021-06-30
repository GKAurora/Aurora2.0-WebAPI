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
from flask.globals import current_app, request
from marshmallow.fields import String
# 
from pkg.extensions import auth
from pkg.schemas import make_res
from pkg.schemas.sdn import SDNGetInSchema, UserListInSchema, UserRouteInSchema
# crawlers
from pkg.crawlers.system.get_single import GetSingle
from pkg.crawlers.users.get_users import GetUserInfoCrawler
from pkg.crawlers.users.get_sites import GetSites
from pkg.crawlers.users.heatmap import HeatMap
from pkg.crawlers.system.speeds import BaseSpeed
from pkg.crawlers.users.get_users import GetUserInfoCrawler
from pkg.crawlers.users.get_err import GetUserErrCrawler
from pkg.crawlers.system.get_all import GetArgs

sdn_bp = APIBlueprint('sdn', __name__)


@sdn_bp.route('/get_sdn_info')
class SDNBaseInfoView(MethodView):
    """获取站点信息和查询质量评估体系健康度趋势

    Args:
        MethodView ([type]): [description]

    Returns:
        [type]: [description]
    """
    @auth_required(auth)
    @input({'site_id': String()}, location='query')
    @doc(summary='获取站点信息', description='传入query string-> site_id，返回对应站点信息，默认返回所有站点')
    def get(self, data):
        site_id = data.get('site_id', '/')
        sites = GetSites.get_data(site_id=site_id)
        return make_res(data=sites)
    
    @auth_required(auth)
    @doc(summary='质量评估体系健康度趋势',
        description='返回总速率，健康度，成功率，漫游达标率等各种健康度信息')
    @input(SDNGetInSchema)
    def post(self, data):
        speeds = BaseSpeed.get_total_speed(**data)
        return make_res(data=speeds)


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
    """用户路径接口（获取用户列表、接入信息）
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
    """获取接入失败数据
    """
    @doc(summary="查询用户接入失败数据")
    # @input()
    def post(self, data):
        res = GetUserErrCrawler.get_data(**data)
        return make_res(data=res)

@sdn_bp.route('/get_total_data')
class GetArgsView(MethodView):

    @auth_required(auth)
    @doc(summary='系统设备多维度数据汇总', description="可用于六角形")
    @input(SDNGetInSchema)
    def post(self, data):
        res = GetArgs.get_data(**data)
        return make_res(data=res)


@sdn_bp.route('/get_trend_single')
class GetSingleView(MethodView):

    @auth_required(auth)
    @doc(summary='质量评估体系单个维度评估结果趋势图')
    @input(SDNGetInSchema)
    def put(self, data):
        res = GetSingle.get_trend_data(**data)
        return make_res(data=res)
    
    @auth_required(auth)
    @input(SDNGetInSchema)
    @doc(summary='查询质量评估体系单个维度数据，包括根因指标')
    def post(self, data):
        res = GetSingle.get_data(**data)
        return make_res(data=res)
        pass




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
    