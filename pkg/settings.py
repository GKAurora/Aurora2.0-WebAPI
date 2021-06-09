# -*- coding: utf-8 -*-
'''
    :file: settings.py
    :author: -Farmer
    :url: https://blog.farmer233.top
    :date: 2021/05/26 16:57:57
'''


# -*- coding: utf-8 -*-

import os
import sys

from sqlalchemy.sql.expression import true

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

# 基本配置
class BaseConfig(object):
    # 鉴权加密密钥（cookie）
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    # 密码重置密钥（找回密码）
    RESET_SECRET_KEY = os.getenv("RESET_SECRET_KEY", "reset dev key")
    # 网盘文件的根目录
    UPLOAD_FOLDER = os.getenv('FILE_SAVE_PATH', os.path.join(basedir, "TestDir"))
    # ORM框架配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 系统标识
    MAIL_SUBJECT_PREFIX = os.getenv("MAIL_SUBJECT_PREFIX", "[CodeShare]")
    # 邮箱服务配置
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Aurora', MAIL_USERNAME)
    # 用户等级划分
    USER_GROUP = os.getenv('USER_GROUP', {
        'user': 0,
        'admin': 9
    })


# 开发环境配置
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_ECHO = True
    # 开发环境使用sqlite作为开发数据库
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))

# 测试配置
class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database

# 生产环境配置
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

# xport配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}