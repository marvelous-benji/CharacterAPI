from flask import jsonify

from project import create_app
from config import get_env
from loguru import logger


app = create_app(get_env("FLASK_CONFIG"))
