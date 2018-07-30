from flask import Flask, render_template, redirect, url_for, session, flash
from flask_mail import Mail, Message
from flask_bootstrap import Bootstrap
from flask_script import Manager, Shell
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import MigrateCommand, Migrate
from threading import Thread

app = Flask(__name__)

app.config['SECRET_KEY'] = "this secret key must be hard to guess"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_SSL'] = True

app.config['MAIL_USERNAME'] = "969793648@qq.com"
app.config['MAIL_PASSWORD'] = "ujawcdqmvkiibcfd"  # 这个是授权码 和 SMTP的授权码有区别吗？
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = "969793648@qq.com"

app.config['FLASKY_ADMIN'] = "969793648@qq.com"

bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


class NameForm(FlaskForm):
    name = StringField("What's you name ? ", validators=[required()])
    submit = SubmitField("Submit")


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship("User", backref='role', lazy='dynamic')

    def __repr__(self):
        return "<Role %r>" % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User %r>" % self.username


@app.errorhandler(400)
def page_not_found():
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error():
    return render_template("500.html"), 500


def make_shell_content():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_content))


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, tempate, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    # msg.body = render_template(tempate + ".txt", **kwargs)
    msg.html = render_template(tempate + ".html", **kwargs)

    # todo 使用多线程发送邮件
    thread = Thread(target=send_async_email, args=(app, msg))
    thread.start()
    return thread


@app.route('/', methods=['POST', 'GET'])  # todo 处理表单的时候，methods一定要加上
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            flash("Pleased to meet you ! ")
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User -- ' + session.get("name"),
                           "mail/new_user", user=user)

        else:
            flash("Nice to meet you again ! ")
        session['name'] = form.name.data
        form.name.data = ""
        return redirect(url_for('index'))
    return render_template("index.html", form=form, name=session.get("name"))


if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()