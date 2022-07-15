import pytest
from .database import client, session


@pytest.fixture()
def test_user(client):
    user_data = {"email": "joe@gmail.com",
                 "password": "123"}
    res = client.post("/users", json=user_data)

    assert res.status_code == 201
    return

def test_create_user(client):
    res = client.post("/users", json={"email":"joe@gmail.com", "password":"123"})
    print(res.json())

    assert res.json().get("email") == "joe@gmail.com"
    assert res.status_code == 201

def test_user_login(client, test_user):
    res = client.post("/login", json={"email": "joe@gmail.com", "password": "123"})
    print(res.json())
    assert res.status_code == 200