import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.126.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '25'))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = 'Lee.T\'s Python Lab'
    FLASKY_MAIL_SENDER = 'Admin <leetsai_test@126.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SSL_REDIRECT = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_POSTS_PER_PAGE = 10
    FLASKY_FOLLOWERS_PER_PAGE = 30
    FLASKY_COMMENTS_PER_PAGE = 30
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    db_user = os.environ.get('db_admin_dev') or 'root'
    db_pass = os.environ.get('db_pass_dev') or '1'
    db_name = os.environ.get('db_name_dev') or 'python'
    db_host = os.environ.get('db_host_dev') or 'docker1'
    db_port = os.environ.get('db_port_dev') or '3306'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql+pymysql://' + db_user + ':' + db_pass + '@' + db_host + ':' \
        + db_port + '/' + db_name
        


class TestingConfig(Config):
    TESTING = True
    db_user = os.environ.get('db_admin_test') or 'root'
    db_pass = os.environ.get('db_pass_test') or '1'
    db_name = os.environ.get('db_name_test') or 'python_test'
    db_host = os.environ.get('db_host_test') or 'docker1'
    db_port = os.environ.get('db_port_test') or '3306'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql+pymysql://' + db_user + ':' + db_pass + '@' + db_host + ':' \
                              + db_port + '/' + db_name

class ProductionConfig(Config):
    db_user = os.environ.get('db_admin') or 'root'
    db_pass = os.environ.get('db_pass') or '1'
    db_name = os.environ.get('db_name') or 'python_pro'
    db_host = os.environ.get('db_host') or 'docker1'
    db_port = os.environ.get('db_port') or '3306'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql+pymysql://' + db_user + ':' + db_pass + '@' + db_host + ':' \
                              + db_port + '/' + db_name
#    SQLALCHEMY_DATABASE_URI = 'mysql://b7feecde952fbd:607c9b8a@us-cdbr-iron-east-04.cleardb.net/heroku_f7ec826bbdafc9a'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig
}
