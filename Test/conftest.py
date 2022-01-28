import pytest
from secrets import token_hex
from flask_jwt_extended import create_access_token

from project import create_app, db
from project.models import FavouriteTracker, User


CHARACTER_ID = "5cd99d4bde30eff6ebccfd0d"


@pytest.fixture(autouse=True)
def app():
    test_app = create_app("test")
    with test_app.app_context():
        db.create_all()
        yield test_app
        db.drop_all()


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def default_user():
    user = User(username="test", email="test@test.com")
    user.password = User.hash_password("test_123")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def default_tracker(default_user):
    tracker = FavouriteTracker(character_id=CHARACTER_ID, user_id=default_user.id)
    db.session.add(tracker)
    db.session.commit()
    return tracker


@pytest.fixture
def token(default_user):
    return create_access_token(identity=default_user)
