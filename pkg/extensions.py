# -*- coding: utf-8 -*-
'''
    :file: extensions.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/05/26 16:59:22
'''
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from apiflask import HTTPTokenAuth
from flask import g, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

db = SQLAlchemy()

auth = HTTPTokenAuth()
mail = Mail()

# 初始化token鉴权插件
@auth.verify_token
def verify_token(token):
    g.user = None
    g.username = None
    try:
        data = Serializer(current_app.config['SECRET_KEY']).loads(token)
    except Exception as e:
        return False
    if "id" in data:
        g.user = data["id"]
        g.username = data['username']
        return True
    return False
