# -*- coding: utf-8 -*-
'''
    :file: sdn_info.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/17 20:30:49
'''
import html
from pkg.crawlers.users.get_floor_device import GetFloorDevice
from marshmallow.validate import Length
from pkg.crawlers.users.get_user_location import GetUserLocation
from apiflask import APIBlueprint, input, output, abort
from apiflask.decorators import auth_required, doc
from flask.views import MethodView
from flask.globals import current_app, request
from apiflask.fields import Integer, String
#
from pkg.extensions import auth
from pkg.schemas import BaseOutSchema, make_res
from pkg.schemas.sdn import GetUserConnErrorInSchema, SDNGetInSchema, UserListInSchema, UserRouteInSchema
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
SITE = '857b706e-67d9-49c0-b3cd-4bd1e6963c07'


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

    @auth_required(auth)
    @doc(summary="查询用户接入失败数据", description='acc_type参数0为有线用户, 1为无线用户')
    @input(GetUserConnErrorInSchema)
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


@auth_required(auth)
@sdn_bp.get('/get_user_location')
@doc(summary='获取终端位置', description='默认站点为深圳，默认level为3; 终端连接强度经过加工;')
@input({
    'site_id': String(),
    'level': Integer()
}, location='query')
def get_user_location(data):
    """获取终端位置，其中终端连接强度已经解析
    """
    res = GetUserLocation.get_data(**data)

    for item in res:
        tmp = html.unescape(res.get(item).get('probeInfo'))
        # 解析payload
        payload = tmp[1:-1]
        user, strength = payload.split("=")
        res[item]['probeInfo'] = {
            'raw': res.get(item).get('probeInfo'),
            'parse': tmp,
            'user': user,
            'strength': strength
        }
    return make_res(data=res)


@auth_required(auth)
@sdn_bp.get('/get_floor_device')
@doc(summary='获取楼层设备', description='默认站点为深圳，默认level为3')
@input({
    'site_id': String(),
    'level': Integer()
}, location='query')
def get_floor_device(data):
    res = GetFloorDevice.get_data(**data)
    return make_res(data=res)
