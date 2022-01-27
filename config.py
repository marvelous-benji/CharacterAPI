import os
import json

#import toastedmarshmallow



basedir = os.path.abspath(os.path.dirname(__name__))


def get_env(variable):
    try:
        return os.environ[variable]
    except KeyError:
        def get_from_file(variable):
            with open("configs.json", "r") as f:
                env_file = json.load(f)
            return env_file[variable]
        return get_from_file(variable)



class BaseConfig:
    SECRET_KEY = get_env('SECRET_KEY')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEFAULT_DB_URI = 'sqlite:///' + os.path.join(basedir, 'default.sqlite')
    #MARSHMALLOW_SCHEMA_DEFAULT_JIT = toastedmarshmallow.Jit
    JSON_SORT_KEYS = False



class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.sqlite') #get_env("DB_DEV_URL")


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'prod.sqlite') #get_env("DB_PROD_URL")



class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tests.sqlite') #get_env("DB_TEST_URL")




configs = {
    "development":DevelopmentConfig,
    "production":ProductionConfig,
    "test":TestingConfig
}