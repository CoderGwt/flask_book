from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
# from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import required
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = "this is the secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)


class NameForm(FlaskForm):
    name = StringField("What is your name ? ", validators=[required()])
    submit = SubmitField("Submit")


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship("User", backref='role', lazy='dynamic')  # 加入lazy='dynamic'参数，禁止自动执行查询

    def __repr__(self):
        return "<Role %r>" % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User %r>" % self.username


# todo 代码中操作数据库
@app.route('/', methods=['GET', 'POST'])
def index():

    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()  # 数据库中查找
        if user is None:  # 如果找不到，就添加进去
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            # session['known'] = False
            flash("Please to meet you ! ")
        else:  # 如果查找的到，就显示出来
            # session['known'] = True
            flash("Nice to meet you again !")
        session['name'] = form.name.data
        form.name.data = ""
        return redirect(url_for("index"))
    return render_template("index.html", form=form,
                           name=session.get("name"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


if __name__ == '__main__':
    app.run(debug=True)