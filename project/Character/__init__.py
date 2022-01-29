'''
Instatiates the character blueprint
and also makes all endpoint in this blueprint
accessible by importing the views module
'''


from flask import Blueprint

character = Blueprint("character", __name__)


from . import views
