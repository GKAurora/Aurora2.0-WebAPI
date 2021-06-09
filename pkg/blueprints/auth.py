# -*- coding: utf-8 -*-
'''
    :file: auth.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/05/31 09:33:34
'''
# Base
from apiflask import APIBlueprint, input, output, abort
from apiflask.decorators import doc
from flask.views import MethodView
from flask.globals import g, current_app
from flask import request
# 
from pkg.schemas import make_res
from pkg.schemas.auth import UserLoginInSchema, UserRegInSchema
from pkg.extensions import db
from pkg.models import User

auth_bp = APIBlueprint('auth', __name__)

@auth_bp.route('/login')
class AuthViews(MethodView):

    @input(UserLoginInSchema)
    @doc(summary='用户登录接口', description="用户登录接口-POST方法", tag='Auth')
    def post(self, data):
        try:
            token = self._login(data.get('username'), data.get('password'))
            return make_res(data={
                "token": token
            })
        except ValueError as ve:
            abort(401, message=str(ve))
        except Exception as e:
            current_app.logger.warning(str(e))
            abort(505)

    @staticmethod
    def _login(username:str, password:str) -> str:
        """A login function.
            
            Arguments:
                username: login username
                password: login user password
            
            return:
                token: the user login token of authority.
        """
        if username is None or password is None:
            raise ValueError("用户名或密码未输入")
        
        user:User = User.query.filter(User.username == username).first()
        if user is None:
            raise ValueError('用户未注册')
        if not user.validate_password(password):
            raise ValueError('密码错误')
        else:
            login_ip = request.host
            user.login_ip = login_ip
            token:str = user.generate_auth_token()
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                current_app.logger.warning(e)
            return token

@auth_bp.route('/reg')
class RegUserViews(MethodView):

    @input(UserRegInSchema(many=True))
    @doc(summary='用户注册', description="通过传数组实现多用户注册", tag='Auth')
    def post(self, datas):
        try:
            if len(datas) < 1:
                raise ValueError('参数缺失')
            self._reg(datas)
            return make_res()
        except ValueError as ve:
            abort(500, str(ve))
        except Exception as e:
            abort(505, str(e))
    
    @staticmethod
    def _reg(datas):
        # 不捕获错误，raise到上层
        try:
            for data in datas:
                user:User = User.query.filter(User.username == data['username']).count()
                if user:
                    raise ValueError(f'{data["username"]}用户已存在')
                db.session.query
                user:User = User()
                user.email = data['email']
                user.username = data['username']
                user.set_password(data['password'])
                user.group = data['group']
                db.session.add(user)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
            

