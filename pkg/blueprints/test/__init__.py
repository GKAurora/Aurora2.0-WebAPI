# -*- coding: utf-8 -*-
'''
    :file: __init__.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/05/26 17:00:58
'''
from pkg.schemas import make_res
from apiflask import APIBlueprint, input, output, abort
from flask.globals import current_app, g
from flask.views import MethodView
from apiflask.decorators import auth_required, doc
# import my app
from pkg.extensions import auth, db
from pkg.schemas.auth_test import UserLoginInSchema
from pkg.models import User

test_bp = APIBlueprint('test', __name__)


@test_bp.route('/')
class AuthTest(MethodView):
    
    @auth_required(auth)
    @doc(description="登录测试接口")
    def get(self):
        return {'msg': f'{g.username} was login!'}

@test_bp.route('/get')
class HuaweiApiTest(MethodView):

    def get(self):
        from pkg.crawlers.users.get_token import GetToken
        token = GetToken.get_token()
        return make_res(data={
            'token': token
        })