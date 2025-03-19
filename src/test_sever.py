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