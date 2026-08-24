from unittest.mock import MagicMock

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.database import get_db
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

def test_redirect_returns_original_url():
    # First, create a short URL
    payload = {
        "url": "https://example.com"
    }
    create_response = client.post("/shorten/", json=payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    short_code = create_response.json()["short_code"]

    redirect_response = client.get(f"/{short_code}", follow_redirects=False)

    assert redirect_response.status_code == status.HTTP_302_FOUND

    assert (redirect_response.headers["location"] == "https://example.com/")

def test_redirect_returns_404_for_nonexistent_short_code():
    response = client.get(
        "/nonexistentcode",
        follow_redirects=False
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()

    assert data["success"] is False

    assert data["error"]["code"] == "URL_NOT_FOUND"

    assert (
        data["error"]["message"]
        == "No URL found for short code: nonexistentcode"
    )

    assert (
        data["error"]["short_code"]
        == "nonexistentcode"
    )
def test_shorten_url_returns_422_when_request_body_is_missing():
    response = client.post("/shorten/")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = response.json()

    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body"]

def test_shorten_url_returns_422_for_empty_url():
    payload = {
        "url": ""
    }

    response = client.post(
        "/shorten/",
        json=payload
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    data = response.json()

    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "url"]


def test_health_check_returns_503_when_database_fails():
    mock_db = MagicMock()
    mock_db.execute.side_effect = SQLAlchemyError("Database unavailable")

    def override_get_db():
        return mock_db

    app.dependency_overrides[get_db] = override_get_db

    try:
        response = client.get("/health")

        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert response.json()["detail"] == "Database connection failed"

    finally:
        app.dependency_overrides.clear()