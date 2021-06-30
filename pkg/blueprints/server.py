# -*- coding: utf-8 -*-
'''
    :file: server.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/30 12:45:18
'''

from email.policy import default
from re import I
from apiflask import APIBlueprint, input, output, abort
from apiflask.decorators import auth_required, doc
from flask.views import MethodView
from flask.globals import current_app, request
from marshmallow.fields import Boolean, Integer, Method
import psutil
#
from pkg.extensions import auth
# schema
from pkg.schemas import BaseOutSchema, make_res

sys_bp = APIBlueprint('sys', __name__)


@sys_bp.route('/cpu')
class GetCpuInfoView(MethodView):

    @auth_required(auth)
    @doc(summary='获取物理cpu利用率', description='默认获取物理cpu速率，percpu参数True时获取逻辑cpu速率，采样时间1s.')
    @input({"percpu": Boolean(default=False, missing=False)}, location='query')
    @output(BaseOutSchema)
    def get(self, data):
        is_percpu = data.get('percpu', False)
        res = psutil.cpu_percent(interval=1, percpu=is_percpu)
        return make_res(data=res)


    # @auth_required(auth)
    # @doc(summary='获取各个逻辑处理器利用率')
    # def post():
    #     pass

@auth_required(auth)
@sys_bp.route('/memory')
@doc(summary='获取内存信息', description='默认获取物理内存，swap参数True时获取交换分区信息')
@input({'swap': Boolean(default=False, missing=False)}, location='query')
@output(BaseOutSchema)
def get_memory_info(data):
    is_swap = data.get('swap', False)
    res = psutil.swap_memory() if is_swap else psutil.virtual_memory()

    return make_res(data={
        "total": res.total,
        "percent": res.percent,
        "used": res.used,
        "free": res.free
    })
