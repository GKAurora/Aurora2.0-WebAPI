# -*- coding: utf-8 -*-
'''
    :file: sdn.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/26 19:02:16
'''

from email.policy import default
from apiflask import Schema
from apiflask.fields import String, Integer
from marshmallow import validate
from marshmallow.validate import Length
from pkg.util.stamp import get_end_stamp, get_start_stamp

# class UserLoginInSchema(Schema):
#     username = String(required=True, validate=Length(5, 10))
#     password = String(required=True, validate=Length(5, 20))

# class UserRegInSchema(UserLoginInSchema):
#     # pass
#     email = Email(required=True)
#     group = Integer(validate=lambda s: s < 10 and s >= 0)
SITE = '857b706e-67d9-49c0-b3cd-4bd1e6963c07'
USER_MAC = ''

class UserListInSchema(Schema):
    site_id = String(default='/', missing='/')
    page = Integer(validate=lambda s : s > 0, default=1, missing=1)
    page_size = Integer(validate=lambda s : s <= 200 and s > 0, default=100, missing=100)
    level = Integer(validate=lambda s : s >= 0 and s < 10, default=1, missing=1)


class UserRouteInSchema(Schema):
    user_mac = String(required=True, validate=Length(15, 20))
    level = Integer(validate=lambda s: s in range(10), default=1, missing=1)
    site_id = String(default='/', missing='/')


class GetSpeedInSchema(Schema):
    site_id = String(validate=Length(min=10), default=SITE, missing=SITE)
    start_time = Integer(default=get_start_stamp(), missing=get_start_stamp())
    end_time = Integer(default=get_end_stamp(), missing=get_end_stamp())

class SDNGetInSchema(Schema):
    site_id = String(validate=Length(min=10), default=SITE, missing=SITE)
    start_time = Integer(default=get_start_stamp(), missing=get_start_stamp())
    end_time = Integer(default=get_end_stamp(), missing=get_end_stamp())
    level = Integer()

class GetUserConnErrorInSchema(Schema):
    acc_type = Integer(validate=lambda s: s in [0, 1])