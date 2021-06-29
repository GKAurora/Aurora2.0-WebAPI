# from apiflask import APIFlask, Schema, input, output, abort
# from apiflask.fields import Integer, String
# from apiflask.validators import Length, OneOf

# Base Model
import os

from werkzeug.exceptions import Unauthorized
from pkg.schemas import make_res
from re import U
import click
from apiflask import APIFlask, abort
from click.decorators import option
from flask import cli

# Import model
from pkg.settings import config
from pkg.extensions import db, mail

# import views
from pkg.blueprints.test import test_bp
from pkg.blueprints.auth import auth_bp
from pkg.blueprints.users import user_bp
from pkg.blueprints.sdn import sdn_bp

# 工厂模式
def create_app(config_name=None)->APIFlask:
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = APIFlask(__name__)
    app.config.from_object(config[config_name])
    register_extensions(app)
    register_blueprints(app)
    register_errors(app)
    register_commands(app)
    return app


def register_extensions(app:APIFlask):
    ''' 初始化扩展 '''
    db.init_app(app)
    mail.init_app(app)


def register_blueprints(app:APIFlask):
    ''' 注册试图函数 '''
    # app.register_blueprint(test_bp, url_prefix='/test')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(sdn_bp, url_prefix='/sdn')


def register_commands(app:APIFlask):
    ''' 注册命令行命令 '''
    @app.cli.command()
    # @click.option("--email", prompt=True, help="The username used to login.")
    @click.option("--username", prompt=True, help="The username used to login.")
    @click.option("--password", prompt=True, hide_input=True, help="The password used to login.")
    def initdb(username, password):
        db.drop_all()
        db.create_all()
        from pkg.models import User
        user:User = User.query.first()
        if user is None:
            user:User = User()
        
        user.username = username
        user.set_password(password)
        user.group = 9
        db.session.add(user)
        db.session.commit()
        click.echo('init dev databases.')
    
    @app.cli.command()
    def test():
        from pkg.crawlers.users import get_user_location
        user_mac = '30-00-00-00-00-22'
        res = get_user_location.GetUserLocation.get_data()
        print(res)




def register_errors(app:APIFlask):
    ''' 注册错误处理钩子 '''
    @app.errorhandler(ValueError)
    def not_Authorization(e):
        return make_res(code=400, message=str(e)), 400
    
    @app.errorhandler(Exception)
    def internal_server_error(e):
        return make_res(code=500, message=str(e)), 500



def register_logging(app:APIFlask):
    ''' 注册日志记录器 '''
    pass

