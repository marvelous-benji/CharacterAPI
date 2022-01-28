from flask import Blueprint

character = Blueprint("character", __name__)


from . import views
