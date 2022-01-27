import bcrypt
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from config import configs





db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from .Auth import auth as auth_blueprint
    from .Character import character as char_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')
    app.register_blueprint(char_blueprint, ulr_prefix='/api/v1/characters')

    return app
