# -*- coding: utf-8 -*-
'''
    :file: auth.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/05/31 09:35:14
'''

from apiflask import Schema
from apiflask.fields import String, Integer, Email
from marshmallow import validate
from marshmallow.validate import Length, Regexp


class UserLoginInSchema(Schema):
    username = String(required=True, validate=Length(5, 10))
    password = String(required=True, validate=Length(5, 20))

class UserRegInSchema(UserLoginInSchema):
    # pass
    email = Email(required=True)
    group = Integer(validate=lambda s: s < 10 and s >= 0)