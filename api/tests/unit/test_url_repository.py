import pytest 
from app.repositories.url_repository import URLRepository
from app.models import URL

@pytest.fixture
def repository(db_session):
    """Create a URLRepository using the test database session."""
    return URLRepository(db=db_session)

def test_create_url(repository):
    url = URL(original_url="https://example.com", short_code="abc12345")
    saved_url = repository.create(url)
    assert saved_url.id is not None
    assert saved_url.original_url == "https://example.com"
    assert saved_url.short_code == "abc12345"
    assert saved_url.created_at is not None

def test_get_by_short_code_returns_url(repository):
    url = URL(original_url="https://example.com", short_code="abc12345")
    repository.create(url)
    result = repository.get_by_short_code("abc12345")
    assert result is not None
    assert result.original_url == "https://example.com"
    assert result.short_code == "abc12345"