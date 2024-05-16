from flask import Flask, render_template, request, redirect, flash, url_for
from utils import load_clubs, load_competitions
from datetime import datetime

app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()
totalPlacesReserved = {}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():

    try:
        club = [
            club for club in clubs if club["email"] == request.form["email"]
        ][0]
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions,
        )
    except IndexError:
        if request.form["email"] == "":
            flash("Please enter your email.", "error")
        else:
            flash("No account related to this email.", "error")
        return render_template("index.html"), 401


@app.route("/book/<competition>/<club>")
def book(competition, club):

    try:

        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [
            c for c in competitions if c["name"] == competition
        ][0]
    except IndexError:
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
                200,
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


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    try:
        competition = [
            c for c in competitions if c["name"] == request.form["competition"]
        ]
        club = [c for c in clubs if c["name"] == request.form["club"]]

        if not competition or not club:
            flash("Competition or club not found.", "error")
            return redirect(url_for("index")), 404
        competition = competition[0]
        club = club[0]
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
        flash("Great-booking complete!")

    return render_template(
        "welcome.html", club=club, competitions=competitions
    )


@app.route("/pointsBoard")
def pointsBoard():

    club_list = sorted(
        clubs, key=lambda club: int(club["points"]), reverse=True
    )

    return render_template("points_board.html", clubs=club_list)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
