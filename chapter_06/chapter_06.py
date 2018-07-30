from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_moment import Moment
# from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import required
from flask_sqlalchemy import SQLAlchemy
from flask_script import Shell
from flask_migrate import MigrateCommand, Migrate  # todo 数据库迁移
from flask_mail import Mail, Message


app = Flask(__name__)

app.config['SECRET_KEY'] = "this is the secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL'] = True

# TODO 这是接收一方的信息还是发送一方的信息？刚才一直用作是发送一方的信息【弄成接收一方的试试看，发送失败】
# todo 有一个疑问， 如果不是发给自己，而是发给别人，会当作是垃圾邮箱处理，这个是怎么回事？
app.config['MAIL_USERNAME'] = "969793648@qq.com"
app.config['MAIL_PASSWORD'] = "ujawcdqmvkiibcfd"  # 这个是授权码 和 SMTP的授权码有区别吗？
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = "969793648@qq.com"

app.config['FLASKY_ADMIN'] = "969793648@qq.com"

# print(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

mail = Mail(app)


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

# todo chapter 6 发送邮件


def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    # msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


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
            print(app.config['FLASKY_ADMIN'])
            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'], "New User", "mail/new_user", user=user)

        else:  # 如果查找的到，就显示出来
            # session['known'] = True
            flash("Nice to meet you again !")
        session['name'] = form.name.data
        form.name.data = ""
        return redirect(url_for("index"))
    return render_template("index.html", form=form, name=session.get("name"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


# 5.10 todo 为shell命令添加上下文
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()