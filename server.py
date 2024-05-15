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
    print(totalPlacesReserved)
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
    print(totalPlacesReserved)
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
    print(totalPlacesReserved)
    competition = [
        c for c in competitions if c["name"] == request.form["competition"]
    ][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]

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
    # Vérifiez si la compétition est déjà dans la structure de données totalPlacesReserved
    if request.form["competition"] not in totalPlacesReserved:
        totalPlacesReserved[request.form["competition"]] = 0

    totalPlacesForCompetition = totalPlacesReserved[
        request.form["competition"]
    ]

    if totalPlacesForCompetition == 12:
        flash(
            "You have already booked 12 places for this competition.", "error"
        )
        return render_template(
            "welcome.html", club=club, competitions=competitions
        )

    if placesRequired > int(club["points"]):
        flash("You don't have enough points.", "error")
    elif placesRequired > placesRemaining:
        flash(
            "Not enough places available, you are trying to book more than the remaining places.",
            "error",
        )
    elif placesRequired < 0:
        flash("You can't book a negative number of places.", "error")
    elif placesRequired > 12:
        flash("You can't book more than 12 places in a competition.", "error")
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


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
