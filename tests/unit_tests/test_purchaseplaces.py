import pytest
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


# Fixture for data club
@pytest.fixture
def clubs():
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        },
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    ]


# Fixture data for compétitions
@pytest.fixture
def competitions():
    return [
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


def test_purchasePlaces_invalid_competition(client, clubs, competitions):
    """
    Test if an invalid competition name is provided, expecting a 404 response.
    """

    data = {
        "competition": "InvalidCompetitionName",
        "club": "Simply Lift",
        "places": "3",
    }
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 404


def test_purchasePlaces_invalid_club(client, clubs, competitions):
    """
    Test if an invalid club name is provided, expecting a 404 response.
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
    """

    data = {
        "competition": "Spring Festival",
        "club": "Iron Temple",
        "places": "20",
    }
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 403


def test_purchasePlaces_negative_places(client, competitions, clubs):
    """
    Test if a negative number of places is specified, expecting a 400 response.
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
    """

    data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": "15",
    }
    response = client.post("/purchasePlaces", data=data)
    assert response.status_code == 403


def test_purchasePlaces_successful_booking(client, competitions, clubs):
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
