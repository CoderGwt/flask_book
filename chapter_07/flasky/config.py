"""
    todo 配置环境
"""


class Config:
    """
        todo 基类，包含通用配置
    """
    SECRET_KEY = "os.environ.get('SECRET_KEY') but it is not be visited"

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True

    MAIL_USERNAME = "969793648@qq.com"
    MAIL_PASSWORD = "ujawcdqmvkiibcfd"  # 这个是授权码 和 SMTP的授权码有区别吗？
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = "969793648@qq.com"

    FLASKY_ADMIN = "969793648@qq.com"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # MAIL_SERVER = 'smtp.qq.com'
    # MAIL_PORT = 465
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = "969793648@qq.com"
    # MAIL_PASSWORD = "ujawcdqmvkiibcfd"  # TODO 这些都是敏感的信息，需要保存到环境变量里
    SQLALCHEMY_DATABASE_URL = "sqlite:///data-dev.sqlite"
    SQLALCHEMY_BINDS = ""


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URL = "sqlite:///data-tests.sqlite"
    SQLALCHEMY_BINDS = ""


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URL = "sqlite:///data.sqlite"
    SQLALCHEMY_BINDS = ""


# todo 注册不同的配置环境
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}