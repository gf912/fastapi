from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from app.main import app
import pytest

@pytest.fixture
def client():
    # run our code before we run our tests
    yield TestClient(app)
    # run our code after we our test finishes

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'Hello World'
    assert res.status_code == 200

def test_create_user(client):
    pass
    # res = client.post("/users", json={"email":"joe@gmail.com", "password":"123"})
    # print(res.json())

    # assert res.json().get("email") == "joe@gmail.com"
    # assert res.status_code == 201
