import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """
    Test the index route, expecting a 200 response.

    This test verifies that the index page (home page) of the application is accessible.

    Steps:
    1. Send a GET request to the root URL ("/").
    2. Check the response status code.

    Expected outcome: The index page should be accessible with a 200 status code.
    """

    response = client.get("/")
    assert response.status_code == 200


def test_no_email(client):
    """
    Test submitting the form without an email, expecting a 401 response.

    This test checks that the application handles form submissions without an email correctly,
    by returning a 401 Unauthorized response.

    Steps:
    1. Send a POST request to "/showSummary" with an empty email field.
    2. Check the response status code.

    Expected outcome: The form submission should be denied with a 401 status code.
    """

    response = client.post("/showSummary", data={"email": ""})
    assert response.status_code == 401


def test_valid_email(client):
    """
    Test submitting the form with a valid email, expecting a 200 response.

    This test checks that the application correctly handles form submissions with a valid email,
    allowing access to the summary page.

    Steps:
    1. Send a POST request to "/showSummary" with a valid email.
    2. Check the response status code.

    Expected outcome: The form submission should be successful with a 200 status code.
    """

    response = client.post(
        "/showSummary", data={"email": "john@simplylift.co"}
    )

    assert response.status_code == 200


def test_invalid_email(client):
    """
    Test submitting the form with an invalid email, expecting a 401 response.

    This test checks that the application handles form submissions with an invalid email correctly,
    by returning a 401 Unauthorized response.

    Steps:
    1. Send a POST request to "/showSummary" with an invalid email.
    2. Check the response status code.

    Expected outcome: The form submission should be denied with a 401 status code.
    """

    data = {"email": "invalid@example.com"}
    response = client.post("/showSummary", data=data)
    assert response.status_code == 401
