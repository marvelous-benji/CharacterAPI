import re
import uuid
from datetime import datetime

from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate, post_load

from project import db, bcrypt


def hex_id():
    return uuid.uuid4().hex


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(50), primary_key=True, index=True, default=hex_id)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True, index=True)
    password = db.Column(db.String(140), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    favorite = db.relationship(
        "FavouriteTracker",
        cascade="all,delete",
        backref=db.backref("liked_by"),
        lazy=True,
    )

    @validates("email")
    def validate_email(self, key, email):
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError("Provided email is not a valid email address")
        return email

    def __repr__(self):
        return f"User('{self.id}','{self.email}')"

    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password)

    @staticmethod
    def verify_password_hash(password_hash, password):
        return bcrypt.check_password_hash(password_hash, password)


class UserSchema(Schema):
    class Meta:
        model = User
        sqla_session = db.session
        ordered = True

    id = fields.String(dump_only=True)
    username = fields.String(validate=validate.Length(min=3), required=True)
    email = fields.Email(required=True)
    password = fields.String(validate=validate.Length(min=7), load_only=True)
    date_created = fields.DateTime(dump_only=True)


class FavouriteTracker(db.Model):
    __tablename__ = "tracker"
    id = db.Column(db.String(50), primary_key=True, index=True, default=hex_id)
    favourite_type = db.Column(db.String(15), default="character")
    character_id = db.Column(db.String(30), nullable=False, index=True)
    quote_id = db.Column(db.String(30), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"FavoriteTracker('{self.character_id}','{self.user_id}')"


class FavouriteTrackerSchema(Schema):
    class Meta:
        models = FavouriteTracker
        sqla_session = db.session
        ordered = True

    id = fields.String(dump_only=True)
    favourite_type = fields.String()
    character_id = fields.String(required=True)
    quote_id = fields.String()
    date_added = fields.DateTime()
    liked_by = fields.Nested(
        "UserSchema",
        only=(
            "username",
            "email",
        ),
    )
