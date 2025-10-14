import pytest
from unittest.mock import patch
from app import app, RegisterUser


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# -------------------
# GET testy
# -------------------
@patch("app.get_games_req")
def test_index(mock_get_games, client):
    mock_get_games.return_value = [{"id": 1, "title": "Test Game"}]
    response = client.get("/")
    assert response.status_code == 200
    assert b"Test Game" in response.data


@patch("app.get_games_req")
def test_game_detail(mock_get_game, client):
    mock_get_game.return_value = {"id": 1, "title": "Test Game"}
    response = client.get("/game/1")
    assert response.status_code == 200
    assert b"Test Game" in response.data


def test_login_get(client):
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_register_get(client):
    response = client.get("/auth/register")
    assert response.status_code == 200


@patch("app.register_user")
@patch("app.RegisterUser.model_validate")
def test_register_post(mock_validate, mock_register, client):
    mock_validate.return_value = RegisterUser(
        username="test", password="pass", repeat_pwd="pass", email="a@b.com"
    )
    mock_register.return_value = True
    data = {
        "username": "test",
        "password": "pass",
        "repeat_pwd": "pass",
        "email": "a@b.com",
    }
    response = client.post("/auth/register", data=data, follow_redirects=True)
    assert response.status_code == 200
