# -*- coding: utf-8 -*-
'''
    :file: __init__.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/05/26 17:04:57
'''

from pkg.utils import get_timestamp
from typing import Any
from apiflask import Schema
from apiflask.fields import String, Integer, Raw
from marshmallow import validate
from marshmallow.validate import Length



def make_res(code:int=200, message:str="ok", data: Any=None) -> dict:
    return {
        "code": code,
        "message": message,
        "data": data,
        "timestamp": get_timestamp()
    }

from apiflask import Schema
from apiflask.fields import String, Integer
from marshmallow import validate
from marshmallow.validate import Length


class BaseOutSchema(Schema):
    code = Integer()
    message = String()
    data = Raw()
    timestamp = Integer()