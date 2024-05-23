import pytest

from flask_testing import TestCase
from server import app, set_test_data

competitions = [
    {
        "name": "test competition soon",
        "date": "2024-10-22 13:30:00",
        "numberOfPlaces": "35",
    }
]

clubs = [
    {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "25",
    },
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
]


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():

            set_test_data(competitions.copy(), clubs.copy())
        yield client


class FunctionalTest(TestCase):

    def create_app(self):
        app.config.from_object("config.TestConfig")

        return app

    def test_login(self):
        """
        Test the login functionality with a valid club email.

        This test checks if a club can successfully log in using a valid email address.
        It ensures that the response status code is 200 and the welcome template is used.

        Steps:
        1. Post a request to /showSummary with a valid club email.
        2. Check the response status code.
        3. Verify that the welcome.html template is used.

        Expected outcome: The club should successfully log in and be redirected to the welcome page.
        """
        response = self.client.post(
            "/showSummary", data={"email": clubs[0]["email"]}
        )
        assert response.status_code == 200
        self.assert_template_used("welcome.html")

    def test_book_future_competion(self):
        """
        Test booking for a future competition.

        This test checks if a club can access the booking page for a future competition.
        It ensures that the response status code is 200 and the booking template is used.

        Steps:
        1. Send a GET request to /book/<competition>/<club> with valid competition and club names.
        2. Check the response status code.
        3. Verify that the booking.html template is used.

        Expected outcome: The booking page for the competition should be displayed.
        """
        response = self.client.get(
            "/book/test%20competition%20soon/Simply%20Lift"
        )
        assert response.status_code == 200
        self.assert_template_used("booking.html")

    def test_purchase_places(self):
        """
        Test purchasing places in a competition.

        This test checks if a club can successfully purchase a specified number of places in a competition.
        It ensures that the response status code is 200.

        Steps:
        1. Post a request to /purchasePlaces with valid competition, club, and places data.
        2. Check the response status code.

        Expected outcome: The places should be successfully purchased, and the response status code should be 200.
        """
        data = {
            "competition": "test competition soon",
            "club": "Simply Lift",
            "places": "12",
        }

        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 200

    def test_places_decrement(self):
        """
        Test if the number of places in a competition is correctly decremented after a successful booking.

        This test checks that after booking a number of places in a competition, the competition's
        number of available places is correctly decremented.

        Steps:
        1. Set initial data for competitions and clubs.
        2. Record initial number of places in the competition.
        3. Perform a booking request with a specified number of places.
        4. Check that the response status code is 200 (OK).
        5. Retrieve the updated number of places in the competition.
        6. Assert that the updated number of places is equal to the initial number minus the booked places.

        Expected outcome: The competition's number of places should be decremented correctly.
        """
        set_test_data(competitions, clubs)
        competition = next(
            c for c in competitions if c["name"] == "test competition soon"
        )
        initial_places = int(competition["numberOfPlaces"])

        print(competitions, clubs)
        print("place initial au debut: ", initial_places)

        data = {
            "competition": "test competition soon",
            "club": "Simply Lift",
            "places": "2",
        }

        response = self.client.post("/purchasePlaces", data=data)

        assert response.status_code == 200

        updated_competition = next(
            c for c in competitions if c["name"] == "test competition soon"
        )
        updated_places = int(updated_competition["numberOfPlaces"])
        print("place initial: ", initial_places)
        print("place mis a jour: ", updated_places)
        print(competitions, clubs)

        assert updated_places == initial_places - 2

    def test_points_decrement(self):
        """
        Test if the points of a club are correctly decremented after a successful booking.

        This test checks that after a club books a number of places in a competition,
        the club's points are correctly decremented by the number of booked places.

        Steps:
        1. Set initial data for competitions and clubs.
        2. Record initial points of the club.
        3. Perform a booking request with a specified number of places.
        4. Check that the response status code is 200 (OK).
        5. Retrieve the updated points of the club.
        6. Assert that the updated points are equal to the initial points minus the booked places.

        Expected outcome: The club's points should be decremented correctly.
        """
        set_test_data(competitions, clubs)
        initial_points = int(
            [
                club["points"]
                for club in clubs
                if club["name"] == "Simply Lift"
            ][0]
        )
        print("Initial club points: ", initial_points)

        data = {
            "competition": "test competition soon",
            "club": "Simply Lift",
            "places": "2",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 200

        updated_points = int(
            [
                club["points"]
                for club in clubs
                if club["name"] == "Simply Lift"
            ][0]
        )
        print("Updated club points: ", updated_points)
        assert updated_points == initial_points - 2

    def test_purchasePlaces_more_than_points(self):
        """
        Test reserving more places than the club has points for, expecting a 403 response.

        This test checks if the application correctly handles a request where a club tries to book more places
        than it has points for. It should return a 403 Forbidden response.

        Steps:
        1. Set initial data for competitions and clubs.
        2. Post a request to /purchasePlaces with a number of places greater than the club's points.
        3. Check the response status code.

        Expected outcome: The request should be denied with a 403 status code.
        """
        set_test_data(competitions, clubs)
        data = {
            "competition": "test competition soon",
            "club": "Simply Lift",
            "places": "30",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 403

    def test_purchasePlaces_more_than_available_places(self):
        """
        Test reserving more places than available in the competition, expecting a 403 response.

        This test checks if the application correctly handles a request where a club tries to book more places
        than are available in the competition. It should return a 403 Forbidden response.

        Steps:
        1. Set initial data for competitions and clubs.
        2. Post a request to /purchasePlaces with a number of places greater than available in the competition.
        3. Check the response status code.

        Expected outcome: The request should be denied with a 403 status code.
        """
        set_test_data(competitions, clubs)
        data = {
            "competition": "test competition soon",
            "club": "Iron Temple",
            "places": "8",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 403

    def test_purchasePlaces_negative_places(self):
        """
        Test reserving a negative number of places, expecting a 400 response.

        This test checks if the application correctly handles a request where a club tries to book a negative
        number of places. It should return a 400 Bad Request response.

        Steps:
        1. Set initial data for competitions and clubs.
        2. Post a request to /purchasePlaces with a negative number of places.
        3. Check the response status code.

        Expected outcome: The request should be denied with a 400 status code.
        """
        set_test_data(competitions, clubs)
        data = {
            "competition": "test competition soon",
            "club": "Simply Lift",
            "places": "-5",
        }
        response = self.client.post("/purchasePlaces", data=data)
        assert response.status_code == 400


if __name__ == "__main__":
    pytest.main()
