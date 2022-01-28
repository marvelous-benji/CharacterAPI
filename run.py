from flask_migrate import Migrate
from flask import Flask, jsonify
from loguru import logger

from project import create_app, db
from config import get_env
from project.models import User, FavouriteTracker


app = create_app(get_env("FLASK_CONFIG"))


migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_processor():
    return dict(app=app, db=db, User=User, FavouriteTracker=FavouriteTracker)


@app.errorhandler(500)
def handle_unexpected_crash(e):
    logger.error(e)
    return jsonify({"status": "failed", "msg": "An error occured"}), 500


@app.errorhandler(404)
def handle_unregistered_url(e):
    logger.error(e)
    return (
        jsonify(
            {"status": "failed", "msg": "The requested url was not found on the server"}
        ),
        404,
    )


@app.errorhandler(405)
def handle_incorrect_method(e):
    logger.error(e)
    return (
        jsonify(
            {
                "status": "failed",
                "msg": "The http method used is not allowed for this route",
            }
        ),
        405,
    )


if __name__ == "__main__":
    app.run()
