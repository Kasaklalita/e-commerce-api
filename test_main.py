from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_all_businesses():
    response = client.get("/businesses")
    assert response.status_code == 200


def test_business_detail():
    response = client.get("/businesses/1")
    assert response.status_code == 200
    assert response.json() == {
        "city": "Moscow",
        "id": 1,
        "description": "Business Description",
        "owner_id": 1,
        "name": "Business 1",
        "region": "Russia",
        "logo": "businessLogo.jpg"
    }
