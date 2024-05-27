import json


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


def search_competition(competition_name, competitions):
    competition = [c for c in competitions if c["name"] == competition_name]
    if len(competition) > 0:
        return competition[0]
    else:
        return None


def search_club_email(email, clubs):
    club = [club for club in clubs if club["email"] == email]
    if len(club) > 0:
        return club[0]
    else:
        return None


def search_club_name(name, clubs):
    club = [club for club in clubs if club["name"] == name]
    if len(club) > 0:
        return club[0]
    else:
        return None


def save_clubs(clubs):
    with open("clubs.json", "w") as c:
        json.dump({"clubs": clubs}, c, indent=4)


def save_competitions(competitions):
    with open("competitions.json", "w") as comps:
        json.dump({"competitions": competitions}, comps, indent=4)
