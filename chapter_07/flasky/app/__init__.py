"""
    todo 程序包的构造文件
"""
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

boostrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    """
        工厂函数
    :param config_name: 程序使用的配置名
    :return: 创建的程序示例
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    boostrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # todo 附加路由和自定义的错误页面、
    # todo 注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app