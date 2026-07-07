import secrets
from app.models import URL
from app.repositories.url_repository import URLRepository

class URLService:
    def __init__(self, repository: URLRepository):

        self.repository = repository
    def generate_short_code(self) -> str:
        # Generate a random URL-safe short code
        SHORT_CODE_BYTE = 6  # Length of the short code
        short_code = secrets.token_urlsafe(SHORT_CODE_BYTE) 
        return short_code

    def create_short_url(self, original_url: str) -> URL:
        # Create a new URL mapping in the database using the URLRepository.
        short_code = self.generate_short_code()
        new_url = URL(original_url=original_url, short_code=short_code)
        saved_url = self.repository.create(new_url)
        return saved_url
