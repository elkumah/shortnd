from fastapi import status
from app.models import URL


def test_create_and_redirect_flow_success(db_session, client):
    """
    Integration test for the complete URL shortening workflow.

    Scenario:
    1. Create a short URL.
    2. Verify the response.
    3. Verify the URL was persisted in PostgreSQL.
    4. Redirect using the generated short code.
    5. Verify the redirect location.
    """

    # ------------------------------------------------------------------
    # Step 1: Create a short URL
    # ------------------------------------------------------------------

    payload = {
        "url": "https://example.com"
    }

    create_response = client.post(
        "/shorten/",
        json=payload
    )

    assert create_response.status_code == status.HTTP_201_CREATED

    # ------------------------------------------------------------------
    # Step 2: Verify response body
    # ------------------------------------------------------------------

    data = create_response.json()

    assert "short_code" in data
    assert "shortened_url" in data

    short_code = data["short_code"]

    assert short_code != ""
    assert data["shortened_url"].endswith(short_code)

    # ------------------------------------------------------------------
    # Step 3: Verify record exists in PostgreSQL
    # ------------------------------------------------------------------

    url_record = (
        db_session.query(URL)
        .filter(URL.short_code == short_code)
        .first()
    )

    assert url_record is not None
    assert url_record.short_code == short_code

    # HttpUrl normalizes the URL with a trailing slash
    assert url_record.original_url == "https://example.com/"

    assert url_record.id is not None
    assert url_record.created_at is not None

    # ------------------------------------------------------------------
    # Step 4: Request redirect
    # ------------------------------------------------------------------

    redirect_response = client.get(
        f"/{short_code}",
        follow_redirects=False,
    )

    # ------------------------------------------------------------------
    # Step 5: Verify redirect response
    # ------------------------------------------------------------------

    assert redirect_response.status_code == status.HTTP_302_FOUND

    assert "location" in redirect_response.headers

    assert (
        redirect_response.headers["location"]
        == "https://example.com/"
    )