import pytest
from server import app, set_test_data

# Données de test pour les compétitions et les clubs
competitions_data = [
    {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25",
    },
    {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13",
    },
]

clubs_data = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "10"},
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
    {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
]


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            set_test_data(competitions_data, clubs_data)  # Reset the data
        yield client


@pytest.fixture
def competitions():
    return competitions_data


@pytest.fixture
def clubs():
    return clubs_data


def test_purchasePlaces_invalid_competition(client, clubs, competitions):
    """
    Test if an invalid competition name is provided, expecting a 404 response.

    This test verifies that when a user tries to book places for a non-existent competition,
    the server responds with a 404 status code indicating the resource was not found.
    """

    data = {
        "competition": "InvalidCompetitionName",
        "club": "Simply Lift",
        "places": "1",
    }
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 404


def test_purchasePlaces_invalid_club(client, clubs, competitions):
    """
    Test if an invalid club name is provided, expecting a 404 response.

    This test verifies that when a user tries to book places with a non-existent club name,
    the server responds with a 404 status code indicating the resource was not found.
    """

    data = {
        "competition": "Spring Festival",
        "club": "InvalidClubName",
        "places": "3",
    }
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 404


def test_purchasePlaces_not_enough_points(client, clubs, competitions):
    """
    Test if a club has insufficient points for booking, expecting a 403 response.

    This test checks that the server prevents a booking if the club does not have enough points.
    The server should respond with a 403 status code indicating that the action is forbidden.
    """

    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "12",
    }
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 403


def test_purchasePlaces_negative_places(client, competitions, clubs):
    """
    Test if a negative number of places is specified, expecting a 400 response.

    This test ensures that the server handles invalid input correctly by rejecting
    bookings where the number of places specified is negative. The server should
    respond with a 400 status code indicating a bad request.
    """

    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "-3",
    }
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 400


def test_purchasePlaces_max_places_exceeded(client, competitions, clubs):
    """
    Test if more places than allowed are specified, expecting a 403 response.

    This test verifies that the server enforces the maximum booking limit. If a user
    tries to book more places than are available in a competition, the server should
    respond with a 403 status code indicating that the action is forbidden.
    """

    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "15",
    }
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 403


def test_purchasePlaces_successful_booking(client, competitions, clubs):
    """
    Test a successful booking, expecting a 200 response.

    This test ensures that a valid booking request (with sufficient points and places available)
    is processed correctly by the server. The server should respond with a 200 status code
    indicating a successful operation.
    """

    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "3",
    }
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 200


def test_purchasePlaces_no_places_specified(client, clubs, competitions):
    """
    Test if no number of places is specified, expecting a 400 response.

    This test checks that the server correctly handles cases where the number of places
    to book is not specified in the request. The server should respond with a 400 status code
    indicating a bad request.
    """

    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "",
    }
    response_no_places = client.post("/purchasePlaces", data=data)
    assert response_no_places.status_code == 400


def test_purchasePlaces_too_many_places(client, clubs, competitions):
    """
    Test if more places are specified than remaining available, expecting a 403 response.

    This test ensures that the server enforces the limit on the number of remaining places in
    a competition. If a user tries to book more places than are available, the server should
    respond with a 403 status code indicating that the action is forbidden.
    """

    data_too_many_places = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "30",
    }
    response_too_many_places = client.post(
        "/purchasePlaces", data=data_too_many_places
    )
    assert response_too_many_places.status_code == 403
