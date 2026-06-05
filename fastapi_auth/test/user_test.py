from fastapi.testclient import TestClient
from main import app  
import pytest
from main import UserLogin
from main import login
from httpx import AsyncClient,ASGITransport
from main import app
from httpx import ASGITransport, AsyncClient
client = TestClient(app)
from unittest.mock import MagicMock, patch


class StubQuery:
    def __init__(self, user):
        self.user = user

    def filter(self, *args):
        return self

    def first(self):
        return self.user
    

class StubDB:
    def __init__(self, user=None):
        self.user = user

    def query(self, model):
        return StubQuery(self.user)


    
def test_login_workflow():
    signup_data = {
        "username": "simpleuser",
        "email": "simple@example.com",
        "password": "mypassword123"
    }
    client.post("/signup", json=signup_data)

    login_response = client.post("/login",json={
            "username": "simpleuser",
            "password": "mypassword123"
        })
    
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"

def test_login_wrong_password():
    bad_login_response = client.post("/login",json={
            "username": "simpleuser",
            "password": "mypassword1"
        })
    assert bad_login_response.status_code == 401
    assert bad_login_response.json()["detail"] == "Incorrect username or password"



def test_login_success_stub(monkeypatch):
    fake_user = type("User", (), {
        "username": "john",
        "hashed_password": "hashed123"
    })
    db = StubDB(user=fake_user)
    user_in = UserLogin(
        username="john",
        password="plain123"
    )
    monkeypatch.setattr("app.main.verify_password", lambda a, b: True)
    result = login(user_in, db)
    assert "access_token" in result
    assert "token_type" in result
    assert result["token_type"] == "bearer"

def test_login_success_with_mock_db():
    db = MagicMock()

    fake_user = MagicMock()
    fake_user.username = "john"
    fake_user.hashed_password = "hashed123"

    db.query().filter().first.return_value = fake_user

    user_in = UserLogin(
        username="john",
        password="plain123"
    )

    with patch("app.main.verify_password", return_value=True):
        result = login(user_in, db)

    assert "access_token" in result
    assert result["token_type"] == "bearer"

