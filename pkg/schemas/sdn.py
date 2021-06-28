# -*- coding: utf-8 -*-
'''
    :file: sdn.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/06/26 19:02:16
'''

from apiflask import Schema
from apiflask.fields import String, Integer
from marshmallow import validate
from marshmallow.validate import Length


# class UserLoginInSchema(Schema):
#     username = String(required=True, validate=Length(5, 10))
#     password = String(required=True, validate=Length(5, 20))

# class UserRegInSchema(UserLoginInSchema):
#     # pass
#     email = Email(required=True)
#     group = Integer(validate=lambda s: s < 10 and s >= 0)

class UserListInSchema(Schema):
    site_id = String()
    page = Integer(validate=lambda s : s > 0)
    page_size = Integer(validate=lambda s : s <= 200 and s > 0)
    level = Integer(validate=lambda s : s >= 0 and s < 10)


class UserRouteInSchema(Schema):
    user_mac = String(required=True, validate=Length(15, 20))
    level = Integer(validate=lambda s: s in range(10))
    site_id = String()


class GetSpeedInSchema(Schema):
    site_id = String(validate=Length(min=10))
    startTime = Integer(validate=Length(equal=13))
    endTime = Integer(validate=Length(equal=13))