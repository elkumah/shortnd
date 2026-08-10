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


    def test_multiple_urls_are_isolated(db_session, client):
       payload1 = {"url": "https://example1.com"}

       response1 = client.post("/shorten/", json=payload1)
       assert response1.status_code == status.HTTP_201_CREATED

       data1 = response1.json()
       assert "short_code" in data1
       assert "shortened_url" in data1
       short_code1 = data1["short_code"]

       payload2 = {"url": "https://github.com"}
       response2 = client.post("/shorten/", json=payload2)
       assert response2.status_code == status.HTTP_201_CREATED
       data2 = response2.json()
       
       assert "short_code" in data2
       assert "shortened_url" in data2
       short_code2 = data2["short_code"]

       url_record1 = (
           db_session.query(URL)
           .filter(URL.short_code == short_code1)
           .first()
       )

       url_record2 = (
           db_session.query(URL)
           .filter(URL.short_code == short_code2)
           .first()
       )

       assert url_record1 is not None
       assert url_record1.short_code == short_code1
       assert url_record1.original_url == "https://example1.com/"

       assert url_record2 is not None
       assert url_record2.short_code == short_code2
       assert url_record2.original_url == "https://github.com/"

       redirect_response1 = client.get(f"/{short_code1}", follow_redirects=False)
       assert redirect_response1.status_code == status.HTTP_302_FOUND
       assert redirect_response1.headers["location"] == "https://example1.com/"

       redirect_response2 = client.get(f"/{short_code2}", follow_redirects=False)
       assert redirect_response2.status_code == status.HTTP_302_FOUND
       assert redirect_response2.headers["location"] == "https://github.com/"