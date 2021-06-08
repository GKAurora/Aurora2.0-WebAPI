# -*- coding: utf-8 -*-
'''
    :file: users.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/05/31 09:32:31
'''
from apiflask import APIBlueprint, input, output, abort
from flask.views import MethodView

user_bp = APIBlueprint('user', __name__)

# @user_bp.route('')