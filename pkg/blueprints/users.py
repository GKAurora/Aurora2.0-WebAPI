# -*- coding: utf-8 -*-
'''
    :file: users.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/05/31 09:32:31
'''
from apiflask.decorators import auth_required, doc
from itsdangerous import exc
from pkg.utils import get_timestamp
from apiflask import APIBlueprint, input, output, abort
from flask.views import MethodView
from flask import g, current_app
#
from pkg.models import User
from pkg.extensions import auth
from pkg.schemas import make_res

user_bp = APIBlueprint('user', __name__)

@user_bp.route('/get_user_info')
class BaseInfoView(MethodView):

    @auth_required(auth)
    @doc(description="登录后获取用户的基本信息")
    def get(self):
        """Return User Base Info.
        Such as last login time, ip.
        """
        user:User = User.query.get(g.user)
        if user is None:
            abort(401)
        msg = self._get_base_info(user)
        return make_res(data=msg)
    
    @staticmethod
    def _get_base_info(user:User):
        return {
            "username": user.username,
            "email": user.email,
            "last_login": user.last_time,
            "type": user.group,
            "ip": user.login_ip
        }
