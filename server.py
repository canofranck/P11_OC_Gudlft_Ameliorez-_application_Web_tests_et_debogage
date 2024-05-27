from flask import Flask, render_template, request, redirect, flash, url_for
from utils import (
    load_clubs,
    load_competitions,
    search_club_email,
    search_club_name,
    search_competition,
    save_clubs,
    save_competitions,
)
from datetime import datetime

app = Flask(__name__)
app.secret_key = "something_special"
app.config.from_object("config.Config")

competitions = load_competitions()
clubs = load_clubs()
totalPlacesReserved = {}


def set_test_data(competitions_data, clubs_data):
    """
    Sets the test data for competitions and clubs.

    Parameters:
    competitions_data (list): List of competitions data.
    clubs_data (list): List of clubs data.
    """

    global competitions
    global clubs
    competitions = competitions_data
    clubs = clubs_data


@app.route("/")
def index():
    """
    Renders the index page.

    Returns:
    Response: The rendered index page.
    """

    return render_template("index.html")


@app.route("/showSummary", methods=["POST", "GET"])
def show_summary():
    """
    Displays the summary page for a club.

    If the request method is GET, it redirects to the index page.
    If the request method is POST, it searches for the club by email
    and displays the welcome page if the club is found, otherwise shows an error.

    Returns:
    Response: The rendered welcome page or an error message.
    """

    if request.method == "GET":
        return redirect(url_for("index"))
    foundclub = search_club_email(request.form["email"], clubs)
    if foundclub == None:
        flash("No account related to this email.", "error")
        return render_template("index.html"), 401
    else:
        club = foundclub
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
        )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Displays the booking page for a specific competition and club.

    Parameters:
    competition (str): The name of the competition.
    club (str): The name of the club.

    Returns:
    Response: The rendered booking page or an error message.
    """

    foundClub = search_club_name(club, clubs)
    foundCompetition = search_competition(competition, competitions)
    if foundCompetition == None or foundClub == None:
        flash("Something went wrong-please try again")
        return (
            render_template(
                "welcome.html",
                club=club,
                competitions=competitions,
                clubs=clubs,
            ),
            400,
        )

    if foundClub and foundCompetition:
        competition_date = datetime.strptime(
            foundCompetition["date"], "%Y-%m-%d %H:%M:%S"
        )
        if competition_date < datetime.now():
            flash("Error: can not purchase a place for past competitions")
            return (
                render_template(
                    "welcome.html",
                    club=foundClub,
                    competitions=competitions,
                    clubs=clubs,
                ),
                400,
            )

        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return (
            render_template(
                "welcome.html",
                club=foundClub,
                competitions=competitions,
                clubs=clubs,
            ),
            400,
        )


@app.route("/purchasePlaces", methods=["POST", "GET"])
def purchasePlaces():
    """
    Handles the place purchasing for a competition.

    If the request method is GET, it redirects to the index page.
    If the request method is POST, it processes the place purchase request
    and updates the competition and club data accordingly.

    Returns:
    Response: The rendered welcome page or an error message.
    """

    if request.method == "GET":
        return redirect(url_for("index"))
    try:
        competition = search_competition(
            request.form["competition"], competitions
        )

        club = search_club_name(request.form["club"], clubs)

        if competition == None or club == None:
            flash("Competition or club not found.", "error")
            return redirect(url_for("index")), 404

    except StopIteration:
        flash("Competition or club not found.", "error")
        return redirect(url_for("index"))

    placesRequired = (
        int(request.form["places"]) if request.form["places"] else None
    )
    placesRemaining = int(competition["numberOfPlaces"])

    if placesRequired is None:
        flash("Please enter the number of places to reserve.", "error")
        return (
            render_template(
                "booking.html", club=club, competition=competition
            ),
            400,
        )

    if request.form["competition"] not in totalPlacesReserved:
        totalPlacesReserved[request.form["competition"]] = 0

    totalPlacesForCompetition = totalPlacesReserved[
        request.form["competition"]
    ]

    if totalPlacesForCompetition == 12:
        flash(
            "You have already booked 12 places for this competition.", "error"
        )
        return (
            render_template(
                "welcome.html", club=club, competitions=competitions
            ),
            403,
        )

    if placesRequired > int(club["points"]):
        flash("You don't have enough points.", "error")
        return (
            render_template(
                "booking.html", club=club, competition=competition
            ),
            403,
        )
    elif placesRequired > placesRemaining:
        flash(
            "Not enough places available, you are trying to book more than the remaining places.",
            "error",
        )
        return (
            render_template(
                "booking.html", club=club, competition=competition
            ),
            409,
        )
    elif placesRequired < 0:
        flash("You can't book a negative number of places.", "error")
        return (
            render_template(
                "booking.html", club=club, competition=competition
            ),
            400,
        )
    elif placesRequired > 12:
        flash("You can't book more than 12 places in a competition.", "error")
        return (
            render_template(
                "booking.html", club=club, competition=competition
            ),
            403,
        )
    elif totalPlacesForCompetition + placesRequired > 12:
        flash(
            "You can't book more than 12 places for this competition.", "error"
        )
    else:
        totalPlacesReserved[request.form["competition"]] += placesRequired
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )
        club["points"] = int(club["points"]) - placesRequired

        # Save changes to JSON files
        # save_competitions(competitions)
        # save_clubs(clubs)

        flash("Great-booking complete!")

    return render_template(
        "welcome.html", club=club, competitions=competitions
    )


@app.route("/pointsBoard")
def pointsBoard():
    """
    Displays the points board.

    Returns:
    Response: The rendered points board page.
    """

    club_list = sorted(
        clubs, key=lambda club: int(club["points"]), reverse=True
    )
    return render_template("points_board.html", clubs=club_list)


@app.route("/logout")
def logout():
    """
    Logs out the user by redirecting to the index page.

    Returns:
    Response: Redirect to the index page.
    """

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
