import os, sys

class Config(object):
    DEBUG = False
    TESTING = False
    REDIS_URL = ''
    UPLOAD_FOLDER= './uploads'

class BaseAppConfig(Config):
    @staticmethod
    def get_base_dir():
        import os, sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        return os.path.abspath(os.path.dirname(__file__))


class TestConfig(BaseAppConfig):

    SQLALCHEMY_SERVER_URI = 'sqlite:///' + os.path.join(BaseAppConfig.get_base_dir(),'tests', 'paranuara_test.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BaseAppConfig.get_base_dir(),'tests', 'paranuara_test.db')

    UPLOAD_FOLDER= './uploads'

class DevelopmentConfig(Config):

    DEBUG = True
    SQLALCHEMY_SERVER_URI = 'sqlite:///' + os.path.join(BaseAppConfig.get_base_dir(), 'paranuara_dev.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BaseAppConfig.get_base_dir(), 'paranuara_dev.db')

    UPLOAD_FOLDER= './uploads'

