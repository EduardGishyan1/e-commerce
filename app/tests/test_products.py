import requests
from app.tests.conftest import BASE_URL


def test_create_product(auth_headers):
    payload = {
        "name": "Laptop",
        "description": "High-end gaming laptop",
        "price": 1500,
        "stock": 10,
        "category": "electronics",
        "image_url": "https://example.com/laptop.png"
    }
    response = requests.post(f"{BASE_URL}/products", headers=auth_headers, json=payload)
    assert response.status_code == 201
    assert "product_id" in response.json()

def test_get_all_products():
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product_details():
    product_id = 1  # Replace with a valid ID
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    assert response.status_code == 200
    assert "name" in response.json()

def test_update_product(auth_headers):
    product_id = 1
    response = requests.put(f"{BASE_URL}/products/{product_id}", headers=auth_headers, json={
        "price": 1400,
        "stock": 15
    })
    assert response.status_code == 200
    assert response.json()["price"] == 1400

def test_delete_product(auth_headers):
    product_id = 1
    response = requests.delete(f"{BASE_URL}/products/{product_id}", headers=auth_headers)
    assert response.status_code == 204