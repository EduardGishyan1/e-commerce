import requests
from app.tests.conftest import BASE_URL

def test_create_order(auth_headers):
    response = requests.post(f"{BASE_URL}/orders", headers=auth_headers, json={
        "product_id": 1,
        "quantity": 2
    })
    assert response.status_code == 201
    assert "order_id" in response.json()

def test_get_order_details(auth_headers):
    order_id = 1
    response = requests.get(f"{BASE_URL}/orders/{order_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "status" in response.json()