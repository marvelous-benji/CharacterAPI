'''
This module contains an object relational
representation of the application database
'''

import re
import uuid
from datetime import datetime

from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate

from project import db, bcrypt


def hex_id():
    '''
    generates unique and random ids
    for primary key usage
    '''

    return uuid.uuid4().hex


class User(db.Model):
    '''
    An object relational representation
    of the users table.
    '''

    __tablename__ = "users"
    id = db.Column(db.String(50), primary_key=True, index=True, default=hex_id)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True, index=True)
    password = db.Column(db.String(140), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    favorite = db.relationship(
        "FavouriteTracker", # creates a one-many relationship with the tracker table
        cascade="all,delete", # implies users favourites should be deleted along with user
        backref=db.backref("liked_by"), # reverse reference from the tracker table to the users'
        lazy=True,
    )

    @validates("email")
    def validate_email(self, key, email):
        '''
        A simple check that the email
        is in valid format
        '''

        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError("Provided email is not a valid email address")
        return email

    def __repr__(self):
        '''
        A readable representation of the User class
        '''
        
        return f"User('{self.id}','{self.email}')"

    @staticmethod
    def hash_password(password):
        '''
        Hashes user password with bcrypt
        Bcrypt is used as it is suitable for 
        password hashing than the SHA derivatives
        '''

        return bcrypt.generate_password_hash(password)

    @staticmethod
    def verify_password_hash(password_hash, password):
        '''
        Verifies that user password is correct
        '''

        return bcrypt.check_password_hash(password_hash, password)


class UserSchema(Schema):
    '''
    A serializer schema for the users table
    '''

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
    '''
    An object relational representation of
    the tracker table.
    '''

    __tablename__ = "tracker"
    id = db.Column(db.String(50), primary_key=True, index=True, default=hex_id)
    favourite_type = db.Column(db.String(15), default="character")
    character_id = db.Column(db.String(30), nullable=False, index=True)
    quote_id = db.Column(db.String(30), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False) # foreign key

    def __repr__(self):
        '''
        A readable representation of the FavouriteTracker class
        '''

        return f"FavoriteTracker('{self.character_id}','{self.user_id}')"


class FavouriteTrackerSchema(Schema):
    '''
    A serializer schema for the tracker table
    '''

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
