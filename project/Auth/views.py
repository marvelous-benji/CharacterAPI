from flask import request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token
from loguru import logger

from project import db, jwt
from . import auth
from ..models import User, UserSchema




@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_payload):
    identity = jwt_payload["sub"]
    return User.query.filter_by(id=identity).one_or_none()



@auth.route("/signup", methods=["POST"])
def signup():
    
    data = request.get_json()
    try:
        try:    
            serializer = UserSchema().load(data).data
            print(serializer)
        except ValidationError as err:
            return jsonify({"status":"failed", "msg":"Your inputs are invalid", "error":err.messages}), 400
        if User.query.filter_by(email=serializer["email"]).first():
            return jsonify({"status":"failed","msg":"You cannot use this email"}), 400
        user = User(email=serializer["email"], username=serializer["username"])
        user.password = User.hash_password(serializer["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"status":"success", "msg":"Sign was successful"}), 201
    except Exception as e:
        logger.error(e)
        return jsonify({"status":"failed","msg":"Unknown error occured"}), 500


@auth.route("/login", methods=["POST"])
def signin():
    data = request.get_json()
    try:    
        serializer = UserSchema(exclude=('username',)).load(data).data
        print(serializer)
    except ValidationError as err:
        return jsonify({"status":"failed", "msg":"Your inputs are invalid", "error":err.messages}), 400
    user = User.query.filter_by(email=serializer["email"]).first()
    if user is None:
        return jsonify({"status":"failed","msg":"Account not found"}), 404
    elif User.check_password_hash(user.password, serializer["password"]):
        access_token = create_access_token(id=user.id)
        return jsonify({"status":"success","msg":"Login was successful","token":access_token}), 200
    else:
        return jsonify({"status":"failed","msg":"Incorrect login credentials"}), 401