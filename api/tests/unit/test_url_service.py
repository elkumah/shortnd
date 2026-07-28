import string

from app.services.url_service import URLService

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