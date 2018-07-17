from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_script import Shell, Manager
from flask_moment import Moment
from wtforms import StringField, SubmitField
from wtforms.validators import required
from flask_migrate import Migrate, MigrateCommand  # 配置Flask-Migrate

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

app.secret_key = "this is the secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  # 每次请求结束后都会自动提交数据库中的变动

# todo 替换上一句，Flask-SQLAlchemy 2.0版本之后被遗弃
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)  # 创建SQLAlchemy 类的实例 db对象，表示程序使用的数据库

bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)
# todo 5.11.1 配置  Flask-Migrate
migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)
# todo 5.11.1 创建迁移仓库 python chapter_05.py db init
# todo 5.11.2 创建迁移脚脚本


# todo 5.6 定义模型
# 在ORM中，模型一般是一个python类，类中的属性对应数据库中的列


class Role(db.Model):
    # __tablename__ 指定了在数据库使用的表名。
    # 如果没有指定，Flask-SQLAlachemy会默认给定一个表名，但是表名没有遵循使用复数形式命名的约定，
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)  # 整型，主键
    name = db.Column(db.String(64), unique=True)  # 字符串型，唯一

    user = db.relationship("User", backref='role', lazy="dynamic")  # 加入lazy，禁止自动执行查询。

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


# todo 数据库操作
# 在python shell 中实际操作

# todo 5.8.1 创建表
"""
创建数据库：
    db.create_all()  创建数据库，如果数据表已存在数据库中db.create_all()不会重新创建或者更新这个表
"""

# todo 5.8.2 插入行
"""
插入行：
    admin_role = Role(name="Admin")
    mod_role = Role(name="Moderator")
    user_role = Role(name="User")
    user_john = User(username="John", role=admin_role)
    usr_susan = User(username="susan", role=user_role)
    user_david = User(username="david", role=user_role)
    
    此时这些对象只存在与python中，还没有写入数据库，因此id尚未赋值
    
通过数据库会话管理对数据库所作的改动 由 db.session表示
    db.session.add_all([admin_role, mod_role, user_role, usr_susan,user_david])

为了把对象写入数据库，最后还要通过db.session.commit()方法提交会话。
    db.session.commit()
  
数据库会话db.session跟之前介绍的Flask session对象没有关系。
数据库会话也叫事务

数据库会话也可 ”回滚“ 调用db.session.rollback()后，
    添加到数据库会话中的所有对象都会还原到他们在数据库时的状态
"""

# todo 5.8.3 修改行
"""
    admin_role.name = "...."
    db.session.add(admin_role)
    db.session.commit()
"""

# todo 5.8.4 删除行
"""
    delete() ...有待补充
"""

# todo 5.8.5 查询行
"""
    query().....有待补充
"""


class NameForm(FlaskForm):
    """
        表单类
    """
    name = StringField("What's your name?", validators=[required()])
    submit = SubmitField("Submit")


# todo 5.9 在视图函数中操作数据库【important】
@app.route('/', methods=['POST', 'GET'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()  # 数据库中查找
        if user is None:  # 如果找不到，就添加
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ""
        return redirect(url_for("index"))

    return render_template("index.html", form=form,
                           name=session.get("name"), known=session.get("known", False))


# todo 5.10 集成Python shell
# @app.shell_context_processor  git 上是这个，但是好像没有效果，所以还是使用一下的manager
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))

# todo 5.11 使用flask-Migrate实现数据库迁移


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()