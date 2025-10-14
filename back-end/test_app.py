import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_liveness(client):
    response = client.get("/liveness")
    assert response.status_code == 200
    assert response.json == {"status": "I am alive"}


@patch("app.check_database")
def test_readiness_ready(mock_check, client):
    mock_check.return_value = True
    response = client.get("/readiness")
    assert response.status_code == 200
    assert response.json == {"status": "I am ready"}


@patch("app.check_database")
def test_readiness_not_ready(mock_check, client):
    mock_check.return_value = False
    response = client.get("/readiness")
    assert response.status_code == 503
    assert response.json == {"status": "I am not ready. Connect database"}
