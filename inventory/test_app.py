import pytest
from unittest.mock import patch
from app import app, inventory
from services import fetch_product_from_openfoodfacts

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_get_single_item(client):
    response = client.get('/inventory/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert "product_name" in data

def test_get_single_item_not_found(client):
    response = client.get('/inventory/999')
    assert response.status_code == 404

def test_add_item(client):
    payload = {
        "product_name": "Organic Oats",
        "brands": "Quaker",
        "quantity": 40,
        "price": 2.50
    }
    response = client.post('/inventory', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["product_name"] == "Organic Oats"
    assert "id" in data

def test_update_item(client):
    payload = {"price": 4.50}
    response = client.patch('/inventory/1', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["price"] == 4.50

def test_delete_item(client):
    # Add a temporary item to delete
    inventory.append({
        "id": 99,
        "product_name": "Temp Item",
        "brands": "Test",
        "quantity": 1,
        "price": 1.00,
        "ingredients_text": ""
    })
    response = client.delete('/inventory/99')
    assert response.status_code == 200

@patch('services.requests.get')
def test_fetch_product_from_openfoodfacts_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Mock Milk",
            "brands": "MockBrand",
            "ingredients_text": "Water, Almonds"
        }
    }
    
    result = fetch_product_from_openfoodfacts(barcode="123456")
    assert result is not None
    assert result["product_name"] == "Mock Milk"
    assert result["brands"] == "MockBrand"