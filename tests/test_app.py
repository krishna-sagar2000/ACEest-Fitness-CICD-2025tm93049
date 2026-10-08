import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

def test_home():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert b"ACEest Fitness and Gym" in response.data
    assert b"Fat Loss" in response.data

def test_program_page():
    client = app.test_client()
    response = client.get('/program/fat-loss')
    assert response.status_code == 200
    assert b"Weekly Workout Chart" in response.data

def test_program_not_found():
    client = app.test_client()
    response = client.get('/program/nonexistent')
    assert response.status_code == 404

def test_signup_empty_name():
    client = app.test_client()
    response = client.post('/signup', data={"name": "", "email": "test@test.com"})
    assert b"Name cannot be empty" in response.data

def test_admin_requires_auth():
    client = app.test_client()
    response = client.get('/admin')
    assert response.status_code == 401
