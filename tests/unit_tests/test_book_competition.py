import pytest
from server import app, competitions, clubs
from datetime import datetime


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_book_past_competition_status_code(client):
    """
    Test booking for a past competition, expecting a 400 response.

    This test checks if the application correctly handles a request to book places
    in a competition that has already passed. It should return a 400 Bad Request response.

    Steps:
    1. Send a GET request to /book/<competition>/<club> with a past competition name.
    2. Check the response status code.

    Expected outcome: The request should be denied with a 400 status code.
    """
    response = client.get("/book/Spring Festival/Simply%20Lift")
    assert response.status_code == 400


def test_book_future_competition_status_code(client):
    """
    Test booking for a future competition, expecting a 200 response.

    This test checks if a club can access the booking page for a future competition.
    It ensures that the response status code is 200 (OK).

    Steps:
    1. Send a GET request to /book/<competition>/<club> with a future competition name.
    2. Check the response status code.

    Expected outcome: The booking page for the competition should be accessible with a 200 status code.
    """
    response = client.get("/book/test competition soon/Simply%20Lift")
    assert response.status_code == 200
