import pytest
from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    payload = response.get_json()
    assert type(payload) is list
    assert len(payload) > 0

def test_create_product(client):
    mock_data = {"name": "Microwave", "price": 200}
    response = client.post('/products', json=mock_data)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["name"] == mock_data["name"]
    assert data["price"] == mock_data["price"]