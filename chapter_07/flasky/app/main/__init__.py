"""
    todo 创建蓝本
"""
from flask import Blueprint

main = Blueprint("main", __name__)  # 实例化Blueprint对象创建蓝本。

# from . import views, errors  # todo 在脚本的末尾导入，避免循环导入依赖。

