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

    # @input(UserLoginInSchema)
    # # @doc(summary='用户登录接口', description="用户登录接口-POST方法", tag='Auth')
    # def post(self, data):
    #     try:
    #         token = self._login(data.get('username'), data.get('password'))
    #         return make_res(data={
    #             "token": token
    #         })
    #     except ValueError as ve:
    #         abort(401, message=str(ve))
    #     except Exception as e:
    #         current_app.logger.warning(str(e))
    #         abort(500)
    
    # @staticmethod
    # def _login(username:str, password:str) -> str:
    #     """A login function.
            
    #         Arguments:
    #             username: login username
    #             password: login user password
            
    #         return:
    #             token: the user login token of authority.
    #     """
    #     if username is None or password is None:
    #         raise ValueError("用户名或密码未输入")
        
    #     user:User = User.query.filter(User.username == username).first()
    #     if user is None:
    #         raise ValueError('用户未注册')
    #     if not user.validate_password(password):
    #         raise ValueError('密码错误')
    #     else:
    #         token:str = user.generate_auth_token()
    #         return token