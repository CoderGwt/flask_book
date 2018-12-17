from . import db

# todo 数据库配置
# create_app.app.config['SECRET_KEY'] = "this secret key must be hard to guess"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.sqlite"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class Role(db.Model):
    """
        todo 数据库 Role
    """
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    users = db.relationship("User", backref='role', lazy='dynamic')

    def __repr__(self):
        return "<Role %r>" % self.name


class User(db.Model):
    """
        todo 数据库User
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return "<User %r>" % self.username
