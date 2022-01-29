'''
This package contains the initialization
of neccessary libraries required for the
successful startup of the application
'''


import bcrypt
from flask import Flask

from flask_caching import Cache
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from config import configs




db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
cache = Cache(config={'CACHE_TYPE': 'simple'})


def create_app(config_name):
    '''
    A factory pattern implementation
    of the Flask app
    '''

    app = Flask(__name__)
    app.config.from_object(configs[config_name]) # configures app instance for different enviroments
    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)

    from .Auth import auth as auth_blueprint
    from .Character import character as char_blueprint

    app.register_blueprint(char_blueprint, url_prefix="/api/v1")
    app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")
    
    return app

