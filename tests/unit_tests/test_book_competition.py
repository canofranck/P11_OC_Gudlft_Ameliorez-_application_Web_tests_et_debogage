import pytest
from server import app, competitions, clubs
from datetime import datetime


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_book_past_competition_status_code(client):
    response = client.get("/book/Fall Classic/Simply%20Lift")
    assert response.status_code == 200  
    assert b"Error: can not purchase a place for past competitions" in response.data

def test_book_future_competition_status_code(client):
    # Modifier la date de la compétition pour une date future
    future_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    competitions.append({"name": "FutureCompetition", "date": future_date,"numberOfPlaces": "45"})

    response = client.get("/book/FutureCompetition/Simply%20Lift")
    assert response.status_code == 200  
    
    
