'''
This module contains all the endpoints
neccessary for getting and setting favourites
'''


from flask import jsonify
from flask_jwt_extended import current_user, jwt_required

from project import db, cache
from . import character
from .utils import character_instance
from ..models import FavouriteTracker



@character.route("/characters", methods=["GET"])
@jwt_required()
@cache.cached(timeout=50)
def return_all_characters():
    '''
    Returns all characters from third-party API
    '''

    response = character_instance.get_all_characters()
    if response is None:
        return jsonify({"status": "failed", "msg": "Service is not availiable"}), 502
    return jsonify({"status": "success", "characters": response["docs"]}), 200


@character.route("/character/<string:id>/quotes", methods=["GET"])
@jwt_required()
@cache.memoize(50)
def return_character_quotes(id):
    '''
    Return quotes belonging to a character
    given its id
    '''

    response = character_instance.get_character_quote(id)
    if response is None:
        return jsonify({"status": "failed", "msg": "Service is not availiable"}), 502
    return jsonify({"status": "success", "characters": response["docs"]}), 200


@character.route("/character/<string:id>/favourite", methods=["POST"])
@jwt_required()
def add_character_to_favourite(id):
    '''
    Adds a character user list of favourites
    '''

    favourite = FavouriteTracker.query.filter_by(
        user_id=current_user.id, character_id=id
    ).first()
    if favourite is not None:
        return (
            jsonify({"status": "failed", "msg": "You've already liked this character"}),
            400,
        )
    favourite = FavouriteTracker(character_id=id, user_id=current_user.id)
    db.session.add(favourite)
    db.session.commit()
    return (
        jsonify(
            {"status": "success", "msg": "Character successfully added as favourite"}
        ),
        200,
    )


@character.route(
    "/character/<string:id>/quotes/<string:quote_id>/favourite", methods=["POST"]
)
@jwt_required()
def add_quote_to_favourite(id, quote_id):
    '''
    Adds a quote and the quote owner information
    to user's list of favourite
    '''

    favourite = FavouriteTracker.query.filter_by(
        user_id=current_user.id, quote_id=quote_id
    ).first()
    if favourite is not None:
        return (
            jsonify({"status": "failed", "msg": "You've already liked this quote"}),
            400,
        )
    response = character_instance.get_quote_by_id(quote_id)
    if response is None:
        return jsonify({"status": "failed", "msg": "This quote is unavailable"}), 404
    char_id = response["docs"][0]["character"]
    favourite = FavouriteTracker(
        character_id=char_id,
        user_id=current_user.id,
        quote_id=quote_id,
        favourite_type="quote",
    )
    db.session.add(favourite)
    db.session.commit()
    return (
        jsonify({"status": "success", "msg": "Quote successfully added as favourite"}),
        200,
    )


@character.route("/favourite", methods=["GET"])
@jwt_required()
@cache.cached(timeout=50)
def get_user_favourites():
    '''
    Returns user's list of favourites
    '''

    users_favourite = []
    items = FavouriteTracker.query.filter_by(user_id=current_user.id).all()
    for favourite in items:
        if favourite.favourite_type == "character":
            response = character_instance.get_character_by_id(favourite.character_id)
            response = response["docs"] if response else "Information not available"
            result = {"favourite_type": "character", favourite.character_id: response}
        else:
            response = character_instance.get_quote_by_id(favourite.quote_id)
            response = response["docs"] if response else "Information not available"
            result = {"favourite_type": "quote", favourite.character_id: response}
        users_favourite.append(result)
    return jsonify({"status": "success", "user_favourite": users_favourite}), 200
