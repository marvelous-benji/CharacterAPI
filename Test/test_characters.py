import json


def test_favouritetracker_db(default_user, default_tracker):
    assert (
        default_tracker.user_id == default_user.id
    ), "Foreinkey constraints must exist"
    assert default_tracker.favourite_type == "character", "Database must be consistent"


def test_characters(client, token):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }
    response = client.get("/api/v1/characters", headers=headers)
    assert response.status_code == 200
    response = json.loads(response.get_data(as_text=True))
    assert "success" == response["status"], "Request must be successful"


def test_character_quote(client, token):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }
    response = client.get(
        "/api/v1/character/5cd99d4bde30eff6ebccfd0d/quotes", headers=headers
    )
    assert response.status_code == 200
    response = json.loads(response.get_data(as_text=True))
    assert "success" == response["status"], "Request must be successful"


def test_favourite_character(client, token):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }
    response = client.post(
        "/characters/5cd99d4bde30eff6ebccfd0d/favourite", headers=headers
    )
    assert response.status_code == 200, "Endpoint must return correct result"


def test_duplicate_favourite_character(client, token, default_tracker):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }
    response = client.post(
        "/characters/5cd99d4bde30eff6ebccfd0d/favourite", headers=headers
    )
    assert response.status_code == 400, "User cannot favourite the same character twice"


def test_favourite_quote(client, token, default_tracker):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }

    response = client.post(
        "/characters/5cd99d4bde30eff6ebccfd0d/quotes/<string:quote_id>/favourite",
        headers=headers,
    )
    assert response.status_code == 200, "Endpoint must return correct result"
    response = json.loads(response.get_data(as_text=True))
    assert response["status"] == "success", "Request must be successful"


def test_empty_favourites(client, token):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }

    response = client.get("/api/v1/favourite", headers=headers)
    assert response.status_code == 200, "Request ought to be successful"
    response = json.loads(response.get_data(as_text=True))
    assert response["user_favourite"] == [], "User has no favourite"


def test_nonempty_favourites(client, token, default_tracker):

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }

    response = client.get("/api/v1/favourite", headers=headers)
    assert response.status_code == 200, "Request ought to be successful"
    response = json.loads(response.get_data(as_text=True))
    assert response["user_favourite"] != [], "User is supposed to have favourite"
