# -*- coding: utf-8 -*-
'''
    :file: auth.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/05/31 09:33:34
'''
# Base
from apiflask import APIBlueprint, input, output, abort
from apiflask.decorators import auth_required, doc
from flask.app import Flask
from flask.views import MethodView
from flask.globals import g, current_app
from flask import request
from sqlalchemy.sql.functions import user
# 
from pkg.schemas import make_res
from pkg.schemas.auth import UserLoginInSchema, UserMessageInSchema, UserMessageOutSchema, UserRegInSchema
from pkg.extensions import db, auth
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
        if not user.state:
            raise ValueError('用户不允许登录')
        else:
            login_ip = request.remote_addr
            print(login_ip)
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
                user:User = User(**data)
                db.session.add(user)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
            

@auth_bp.post('/user')
@auth_required(auth)
@input(UserMessageInSchema)
def controller(data):
    user:User = User.query.get(g.user)

    if data.get('password') != None:
        user.set_password(data.get('password'))
    if data.get('email') != None:
        user.email = data.get('email')
    if data.get('state') != None:
        user.state = data.get('state')
    db.session.add(user)
    db.session.commit()
    return make_res()


@auth_bp.get('/get')
@auth_required(auth)
@output(UserMessageOutSchema(many=True))
def get_users():
    users = User.query.all()
    return users
