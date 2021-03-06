'''
Tests the users table and authentication endpoints
'''


import json

from project.models import User

def test_user_db(default_user):
    '''
    Tests users table
    '''

    assert default_user.username == "test"
    assert User.verify_password_hash(default_user.password, "test_123") is True
    assert default_user.email == "test@test.com"


def test_signup(client):
    '''
    Tests signup endpoint
    '''

    data = {"email": "test01@test.com", "password": "test_123", "username": "tester"}
    headers = {"Content-Type": "application/json"}
    response = client.post(
        "/api/v1/auth/signup", headers=headers, data=json.dumps(data)
    )
    assert response.status_code == 201
    response = json.loads(response.get_data(as_text=True))
    assert "success" == response["status"]


def test_login(client):
    '''
    Tests login endpoint
    '''
    
    data = {"email": "test@test.com", "password": "test_123"}
    headers = {"Content-Type": "application/json"}
    response = client.post("/api/v1/auth/login", headers=headers, data=json.dumps(data))
    assert response.status_code == 200
    response = response.get_data(as_text=True)
    assert "token" in response
