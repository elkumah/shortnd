import string
from unittest.mock import Mock, patch

from app.services.url_service import URLService
from app.models import URL
from app.schemas import URLRequest

def test_generate_short_code_returns_code():
    service = URLService(repository=None)  # Pass None for repository as it's not needed for this test
    short_code = service.generate_short_code()
    assert short_code is not None
    assert isinstance(short_code, str)

def test_short_code_has_correct_length():
    service = URLService(repository=None)
    short_code = service.generate_short_code()
    assert len(short_code) >= 6  # Check minimum length
    assert len(short_code) <= 20  # Check maximum length

def test_generate_short_code_is_unique():
    service = URLService(repository=None)
    first_code = service.generate_short_code()
    second_code = service.generate_short_code()
    assert first_code != second_code  # Ensure two generated codes are not the same

def test_generate_short_code_contains_url_safe_characters():
    service = URLService(repository=None)
    short_code = service.generate_short_code()
    url_safe_characters = string.ascii_letters + string.digits + "-_"
    assert all(char in url_safe_characters for char in short_code)  # Check if all characters are URL-safe

def test_create_short_url_successful_creates_new_url():
    mock_repository = Mock()
    service = URLService(repository=mock_repository)
  
    request = URLRequest(
        url="https://example.com"
    )

    mock_repository.get_by_short_code.return_value = None

    saved_url = URL(
        original_url="https://example.com",
        short_code="abc12345"
    )

    mock_repository.create.return_value = saved_url

    # Act
    with patch.object(
        URLService,
        "generate_short_code",
        return_value="abc12345"
    ):
        result = service.create_short_url(request)

    # Assert
    assert result.original_url == "https://example.com"
    assert result.short_code == "abc12345"

    mock_repository.get_by_short_code.assert_called_once_with(
        "abc12345"
    )

    mock_repository.create.assert_called_once()

# Test that create new url generates a new short code if the generated one already exists in the database
def test_create_short_url_generates_new_code_when_collision_occurs():
    mock_repository = Mock()
    service = URLService(repository=mock_repository)

    request = URLRequest(
        url="https://example.com"
    )

    # Simulate a collision by returning a URLModel for the first generated short code
    mock_repository.get_by_short_code.side_effect = [
        URL(original_url="https://example.com", short_code="abc12345"),  # First call returns an existing URL
        None  # Second call returns None, indicating no collision
    ]

    saved_url = URL(
        original_url="https://example.com",
        short_code="def67890"
    )

    mock_repository.create.return_value = saved_url

    # Act
    with patch.object(
        URLService,
        "generate_short_code",
        side_effect=["abc12345", "def67890"]  # First call generates a colliding code, second call generates a unique code
    ):
        result = service.create_short_url(request)

    # Assert
    assert result.original_url == "https://example.com"
    assert result.short_code == "def67890"

    assert mock_repository.get_by_short_code.call_count == 2  # Ensure it checked for collisions twice

    # test_create_short_url_propagates_repository_exception()
    def test_create_short_url_propagates_repository_exception():
        mock_repository = Mock()
        service = URLService(repository=mock_repository)

        request = URLRequest(
            url="https://example.com"
        )

        # Simulate an exception being raised by the repository's create method
        mock_repository.create.side_effect = Exception("Database error")

        # Act & Assert
        with patch.object(
            URLService,
            "generate_short_code",
            return_value="abc12345"
        ):
            try:
                service.create_short_url(request)
                assert False, "Expected an exception to be raised"
            except Exception as e:
                assert str(e) == "Database error"  # Ensure the exception message matches