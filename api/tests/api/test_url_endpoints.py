from fastapi.testclient import TestClient
from fastapi import status
from app.config import settings
from app.main import app

client = TestClient(app)


def test_root_returns_api_information():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Secure URL Shortener API"
    assert data["version"] == "1.0.0"


def test_health_check_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"

def test_shorten_url_successfully_creates_short_url():
    payload = {
        "url": "https://example.com"
    }
    response = client.post("/shorten/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()

    assert "short_code" in data
    assert "shortened_url" in data

    assert data["short_code"] != ""
    assert data["shortened_url"].startswith(settings.BASE_URL)

def test_shorten_url_returns_422_for_invalid_url():
    payload = {
        "url": "invalid-url"
    }
    response = client.post("/shorten/", json=payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = response.json()
    assert "detail" in data

    assert data["detail"][0]["loc"] == ["body", "url"]

def test_shorten_url_returns_422_when_url_field_is_missing():
    payload = {}

    response = client.post(
        "/shorten/",
        json=payload
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = response.json()

    assert "detail" in data

    assert data["detail"][0]["loc"] == ["body", "url"]

    assert data["detail"][0]["type"] == "missing"