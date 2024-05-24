import json


def load_clubs():
    with open("clubs.json") as c:
        list_of_clubs = json.load(c)["clubs"]
        return list_of_clubs


def load_competitions():
    with open("competitions.json") as comps:
        list_of_competitions = json.load(comps)["competitions"]
        return list_of_competitions


def save_clubs(clubs):
    with open("clubs.json", "w") as c:
        json.dump({"clubs": clubs}, c, indent=4)


def save_competitions(competitions):
    with open("competitions.json", "w") as comps:
        json.dump({"competitions": competitions}, comps, indent=4)
