import requests
from app.tests.conftest import BASE_URL

def test_get_user_profile(auth_headers):
    user_id = 1  # Replace with a valid user ID
    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "email" in response.json()

def test_update_user_profile(auth_headers):
    user_id = 1
    response = requests.put(f"{BASE_URL}/users/{user_id}", headers=auth_headers, json={
        "name": "Updated Name"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"