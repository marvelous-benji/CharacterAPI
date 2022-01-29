'''
Instatiates the authentication blueprint
and also makes all endpoint in this blueprint
accessible by importing the views module
'''



from flask import Blueprint

auth = Blueprint("auth", __name__)


from . import views
