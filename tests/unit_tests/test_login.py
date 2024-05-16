import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):

    response = client.get("/")
    assert response.status_code == 200


def test_no_email(client):
    response = client.post("/showSummary")
    assert response.status_code == 400


def test_valid_email(client):

    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}
    )

    assert response.status_code == 200


def test_invalid_email(client):
    data = {"email": "invalid@example.com"}
    response = client.post("/showSummary", data=data)
    assert response.status_code == 401
