import pytest
from src.server import AppFactory
import os

@pytest.fixture
def app():
    basedir = os.path.abspath(os.path.dirname(__file__)) # Store absolute path to current directory
    test_app = AppFactory(basedir)
    return test_app

# Pytest fixture to create and yield a test client
# This client simulates HTTP requests during tests.
@pytest.fixture
def client(app):
    with app.app.test_client() as client:
        yield client
        app.db.session.remove()
        app.db.drop_all()

# Integration test for GET /products endpoint
def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200 # Assuring response code is HTTP 200
    payload = response.get_json()
    assert type(payload) is list # Assuring the payload type is a list
    assert len(payload) > 0 # Assuring non-empty payload
    assert all("id" in p and "name" in p and "price" in p for p in payload) # Assuring each product has id, name, and price fields

# Integration test for POST /products endpoint
def test_create_product(client):
    mock_data = {"name": "Microwave", "price": 200} # Preparing mock request data
    response = client.post('/products', json=mock_data)
    assert response.status_code == 201 # Assuring response code is HTTP 201
    data = response.get_json() 
    assert "id" in data # Assuring response payload contains id field
    assert data["name"] == mock_data["name"] # Assuring that the returned product's name matches that of the mock
    assert data["price"] == mock_data["price"] # Assuring that the returned product's price matches that of the mock

# Integration test for POST /sales endpoint
def test_make_sale(client):
    # Prepare a sale payload with two line items and a flat discount
    sale_payload = {
        "line_items": [
            {"id": 1, "quantity": 2},
            {"id": 2, "quantity": 1} 
        ],
        "discount": 10  # A flat discount to be distributed among line items
    }
    response = client.post('/sales', json=sale_payload)
    assert response.status_code == 200
    data = response.get_json()
    
    # Check that the response contains the expected keys
    assert "line_items" in data
    assert "total_sale_price" in data
    
    # Verify that each processed line item includes a discount value
    for item in data["line_items"]:
        assert "id" in item
        assert "quantity" in item
        assert "price" in item
        assert "discount" in item and item["discount"] == 10/len(data["line_items"])

    # - For product id=1: 2 * 100 = 200
    # - For product id=2: 1 * 49.99 = 49.99
    # The total_sale_price should be the sum of these (discount isn't subtracted from total_sale_price)
    expected_total = 200 + 49.99
    # Use a tolerance for floating point arithmetic
    assert data["total_sale_price"] - expected_total == 0