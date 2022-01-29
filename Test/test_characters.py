'''
Tests the tracker table and characters endpoint
'''


import json


def test_favouritetracker_db(default_user, default_tracker):
    '''
    Tests the tracker table
    '''

    assert (
        default_tracker.user_id == default_user.id
    ), "Foreinkey constraints must exist"
    assert default_tracker.favourite_type == "character", "Database must be consistent"


def test_characters(client, token):
    '''
    Tests the get all character endpoint
    '''

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }
    response = client.get("/api/v1/characters", headers=headers)
    assert response.status_code == 200
    response = json.loads(response.get_data(as_text=True))
    assert "success" == response["status"], "Request must be successful"


def test_character_quote(client, token):
    '''
    Tests the get character quote endpoint
    '''

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
    '''
    Tests the add favourite character endpoint
    '''

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }
    response = client.post(
        "/api/v1/character/5cd99d4bde30eff6ebccfd0d/favourite", headers=headers
    )
    assert response.status_code == 200, "Endpoint must return correct result"


def test_duplicate_favourite_character(client, token, default_tracker):
    '''
    Tests that duplicate favourite character is not allowed
    '''

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }
    response = client.post(
        "/api/v1/character/5cd99d4bde30eff6ebccfd0d/favourite", headers=headers
    )
    assert response.status_code == 400, "User cannot favourite the same character twice"


def test_favourite_quote(client, token, default_tracker):
    '''
    Tests the add favourite quote endpoint
    '''

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }

    response = client.post(
        "/api/v1/character/5cd99d4bde30eff6ebccfd0d/quotes/5cd96e05de30eff6ebccf124/favourite",
        headers=headers,
    )
    assert response.status_code == 200, "Endpoint must return correct result"
    response = json.loads(response.get_data(as_text=True))
    assert response["status"] == "success", "Request must be successful"


def test_empty_favourites(client, token):
    '''
    Tests the get all user favourite enpoint
    when user has no favourite
    '''

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }

    response = client.get("/api/v1/favourite", headers=headers)
    assert response.status_code == 200, "Request ought to be successful"
    response = json.loads(response.get_data(as_text=True))
    print(response)
    assert response["user_favourite"] == [], "User has no favourite"


def test_nonempty_favourites(client, token, default_tracker):
    '''
    Tests the get all user favourite enpoint
    when user has favourite
    '''

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(token),
    }

    response = client.get("/api/v1/favourite", headers=headers)
    assert response.status_code == 200, "Request ought to be successful"
    response = json.loads(response.get_data(as_text=True))
    assert response["user_favourite"] != [], "User is supposed to have favourite"
