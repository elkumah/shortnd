import string
from unittest.mock import Mock, patch

import pytest

from app.exceptions.custom_exceptions import URLNotFoundException
from app.models import URL
from app.services.url_service import (
    MAX_RETRY_ATTEMPTS,
    URLService,
)


@pytest.fixture
def mock_repository():
    """Create a mock repository for unit tests."""
    return Mock()


@pytest.fixture
def service(mock_repository):
    """Create a URLService using a mocked repository."""
    return URLService(repository=mock_repository)


# --------------------------------------------------------------------
# generate_short_code()
# --------------------------------------------------------------------

def test_generate_short_code_returns_string(service):
    short_code = service.generate_short_code()

    assert short_code is not None
    assert isinstance(short_code, str)


def test_generate_short_code_is_unique(service):
    first_code = service.generate_short_code()
    second_code = service.generate_short_code()

    assert first_code != second_code


def test_generate_short_code_contains_url_safe_characters(service):
    short_code = service.generate_short_code()

    url_safe_characters = string.ascii_letters + string.digits + "-_"

    assert all(char in url_safe_characters for char in short_code)


# --------------------------------------------------------------------
# generate_unique_short_code()
# --------------------------------------------------------------------

def test_generate_unique_short_code_returns_unique_code(
    service,
    mock_repository,
):
    mock_repository.get_by_short_code.return_value = None

    with patch.object(
        URLService,
        "generate_short_code",
        return_value="abc12345",
    ):
        short_code = service.generate_unique_short_code()

    assert short_code == "abc12345"

    mock_repository.get_by_short_code.assert_called_once_with(
        "abc12345"
    )


def test_generate_unique_short_code_retries_after_collision(
    service,
    mock_repository,
):
    mock_repository.get_by_short_code.side_effect = [
        URL(
            original_url="https://example.com",
            short_code="abc12345",
        ),
        None,
    ]

    with patch.object(
        URLService,
        "generate_short_code",
        side_effect=["abc12345", "def67890"],
    ):
        short_code = service.generate_unique_short_code()

    assert short_code == "def67890"

    assert mock_repository.get_by_short_code.call_count == 2


def test_generate_unique_short_code_raises_runtime_error_after_max_retries(
    service,
    mock_repository,
):
    mock_repository.get_by_short_code.return_value = URL(
        original_url="https://example.com",
        short_code="collision",
    )

    with patch.object(
        URLService,
        "generate_short_code",
        return_value="collision",
    ), pytest.raises(RuntimeError) as exc_info:
        service.generate_unique_short_code()

    assert (
        str(exc_info.value)
        == f"Failed to generate a unique short code after "
        f"{MAX_RETRY_ATTEMPTS} attempts."
    )


# --------------------------------------------------------------------
# create_short_url()
# --------------------------------------------------------------------

def test_create_short_url_success(
    service,
    mock_repository,
):
    saved_url = URL(
        original_url="https://example.com",
        short_code="abc12345",
    )

    mock_repository.get_by_short_code.return_value = None
    mock_repository.create.return_value = saved_url

    with patch.object(
        URLService,
        "generate_short_code",
        return_value="abc12345",
    ):
        result = service.create_short_url(
            "https://example.com"
        )

    assert result.original_url == "https://example.com"
    assert result.short_code == "abc12345"

    mock_repository.create.assert_called_once()


def test_create_short_url_propagates_repository_exception(
    service,
    mock_repository,
):
    mock_repository.get_by_short_code.return_value = None

    mock_repository.create.side_effect = Exception(
        "Database error"
    )

    with patch.object(
        URLService,
        "generate_short_code",
        return_value="abc12345",
    ), pytest.raises(Exception, match="Database error"):
        service.create_short_url(
            "https://example.com"
        )


# --------------------------------------------------------------------
# get_url_by_short_code()
# --------------------------------------------------------------------

def test_get_url_by_short_code_returns_url(
    service,
    mock_repository,
):
    url = URL(
        original_url="https://example.com",
        short_code="abc12345",
    )

    mock_repository.get_by_short_code.return_value = url

    result = service.get_url_by_short_code(
        "abc12345"
    )

    assert result == url

    mock_repository.get_by_short_code.assert_called_once_with(
        "abc12345"
    )


def test_get_url_by_short_code_raises_url_not_found_exception(
    service,
    mock_repository,
):
    mock_repository.get_by_short_code.return_value = None

    with pytest.raises(
        URLNotFoundException,
        match="No URL found for short code: abc12345",
    ):
        service.get_url_by_short_code("abc12345")

def test_create_short_url_propagates_runtime_error(repository):
    service = URLService(repository)

    repository_error = RuntimeError(
        "Failed to generate a unique short code after 5 attempts."
    )

    with patch.object(
        service,
        "generate_unique_short_code",
        side_effect=repository_error,
    ):
        with pytest.raises(RuntimeError, match="Failed to generate a unique short code"):
            service.create_short_url("https://example.com")