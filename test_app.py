import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# Test 1 - check the homepage loads
def test_homepage(client):
    res = client.get("/")
    assert res.status_code == 200

# Test 2 - check health endpoint returns ok
def test_health(client):
    res = client.get("/health")
    data = res.get_json()
    assert res.status_code == 200
    assert data["status"] == "ok"

# Test 3 - check invalid breed gives an error
def test_invalid_breed(client):
    res = client.get("/api/dog/invalidbreed")
    assert res.status_code == 400

# Test 4 - check status endpoint has correct keys
def test_status(client):
    res = client.get("/status")
    data = res.get_json()
    assert "database" in data
    assert "dog_api" in data