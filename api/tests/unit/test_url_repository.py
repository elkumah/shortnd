import pytest
from sqlalchemy.exc import IntegrityError

from app.models import URL


def test_create_url(repository):
    url = URL(
        original_url="https://example.com",
        short_code="create01",
    )

    saved_url = repository.create(url)

    assert saved_url.id is not None
    assert saved_url.original_url == "https://example.com"
    assert saved_url.short_code == "create01"
    assert saved_url.created_at is not None

def test_get_by_short_code_returns_url(repository):
    url = URL(
        original_url="https://example.com",
        short_code="get00001",
    )

    repository.create(url)

    result = repository.get_by_short_code("get00001")

    assert result is not None
    assert result.original_url == "https://example.com"
    assert result.short_code == "get00001"

def test_get_by_short_code_returns_none_when_not_found(repository):
    result = repository.get_by_short_code("does-not-exist")
    assert result is None

def test_create_duplicate_short_code_raises_integrity_error(
    repository,
):
    url1 = URL(
        original_url="https://example.com",
        short_code="dup12345",
    )

    url2 = URL(
        original_url="https://example.org",
        short_code="dup12345",
    )

    repository.create(url1)

    with pytest.raises(IntegrityError):
        repository.create(url2)

    # Reset the session after the failed commit
    repository.db.rollback()

def test_create_generates_uuid_and_timestamp(repository):
    url = URL(original_url="https://example.com", short_code="uid12345")
    saved_url = repository.create(url)
    assert saved_url.id is not None
    assert saved_url.created_at is not None