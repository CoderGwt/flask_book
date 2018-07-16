from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
"""
    Flask-SQLAlchemy 是一个关系型数据库的框架
        提供了高层的ORM，也提供了使用数据库原生SQL的底层功能
        
        数据库使用URL指定：
            mysql: mysql://username:password@hostname/database
            
"""

# todo 5.5 使用Flask-SQLAlchemy 扩展管理数据库
# 配置数据库
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)  # 创建SQLAlchemy 类的实例 db对象，表示程序使用的数据库

# todo 5.6 定义模型
# 在ORM中，模型一般是一个python类，类中的属性对应数据库中的列


class Role(db.Model):
    # __tablename__ 指定了在数据库使用的表名。
    # 如果没有指定，Flask-SQLAlachemy会默认给定一个表名，但是表名没有遵循使用复数形式命名的约定，
    __tablename = "roles"
    id = db.Column(db.Integer, primary_key=True)  # 整型，主键
    name = db.Column(db.String(64), unique=True)  # 字符串型，唯一

    user = db.relationship("User", backref='role')

    def __repr__(self):
        return "<Role %r>" % self.name


'''
    db.Column 类构造函数的第一个参数是数据库列中的模型属性的类型。常见的有很多。其余参数指定属性的配置选项
'''


class User(db.Model):
    __tablename__ = "users"  # 表名
    id = db.Column(db.Integer, primary_key=True)  # 整型，主键
    username = db.Column(db.String(64), unique=True, index=True)  # 为这列创建索引，提高查询效率

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))  # todo 外键
    # 传给db.ForeignKey(’roles.id') 表示这个是roles表中行id的值

    def __repr__(self):
        return "<User %r>" % self.username


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
