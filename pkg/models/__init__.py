# -*- coding: utf-8 -*-
'''
    :file: __init__.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/05/26 17:06:42
'''
from pkg.utils import get_timestamp
from flask.globals import current_app
from pkg.extensions import db
import sqlalchemy as sa
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import BadSignature, SignatureExpired, TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime


class User(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    # 注册必备
    username = sa.Column(sa.String(20))
    password_hash = sa.Column(sa.String(128))
    email = sa.Column(sa.String(260))
    group = sa.Column(sa.Integer, default=0)
    state = sa.Column(sa.Boolean, default=True)
    # 后期动态
    login_ip = sa.Column(sa.String(21))
    last_time = sa.Column(
        sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        if len(password) < 5:
            raise ValueError('密码长度不够')
        self.password_hash = generate_password_hash(password)
    
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_password(self):
        return self.password_hash
    
    password = property(get_password, set_password)

    # 登录成功返回鉴权令牌（生成token）
    def generate_auth_token(self, expiration=3600 * 24 * 7):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({
            'id': self.id,
            'username': self.username
        }).decode()

    # 鉴权（验证token）
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user