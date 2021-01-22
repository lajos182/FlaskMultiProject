import os
from datetime import timedelta

from redis import Redis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_db_uri(dbinfo):
    engine = dbinfo.get('ENGINE') or 'sqlite'
    driver = dbinfo.get('DRIVER') or 'sqlite'
    user = dbinfo.get('USER') or ''
    password = dbinfo.get('PASSWORD') or ''
    host = dbinfo.get('HOST') or ''
    port = dbinfo.get('PORT') or ''
    name = dbinfo.get('NAME') or ''
    if engine == 'sqlite':
        return f'{engine}:///{os.path.join(BASE_DIR, name)}'
    return f'{engine}+{driver}://{user}:{password}@{host}:{port}/{name}'

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # session设置
    SECRET_KEY = 'o5QC16j0SPqoUiO/i1nunQ8VtvZvaEV+iQ5dZoZ5XfA='
    SESSION_TYPE = 'redis'
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    # SESSION_USE_SIGNER: sessionkey进行加密处理, 使用secret_key, 默认False
    # sessionkey对应的前缀
    SESSION_KEY_PREFIX = 'FlaskMultiProject:'
    # session连接位置, 默认127.0.0.1:6379
    SESSION_REDIS = Redis(host='127.0.0.1', port=6379, db=1, password=None)
    # SESSION_FILE_THRESHOLD： session最大缓存条数，默认500

class DevelopConfig(Config):
    DEBUG = True
    dbinfo = {
        'ENGINE': 'sqlite',
        'DRIVER': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'NAME': 'GPIFlask'
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)

class TestingConfig(Config):
    TESTING = True
    dbinfo = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'jiang',
        'HOST': 'localhost',
        'PORT': 3306,
        'NAME': 'GPIFlask'
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)

class StagingConfig(Config):
    dbinfo = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'jiang',
        'HOST': 'localhost',
        'PORT': 3306,
        'NAME': 'GPIFlask'
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)

class ProductConfig(Config):
    dbinfo = {
        'ENGINE': 'mysql',
        'DRIVER': 'pymysql',
        'USER': 'root',
        'PASSWORD': 'jiang',
        'HOST': 'localhost',
        'PORT': 3306,
        'NAME': 'GPIFlask'
    }
    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)

envs = {
    'develop': DevelopConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'product': ProductConfig,
    'default': DevelopConfig
}