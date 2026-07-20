import secrets

from ..models import URL
from ..repositories.url_repository import URLRepository
from ..exceptions import URLNotFoundException

SHORT_CODE_BYTES = 6
MAX_RETRY_ATTEMPTS = 5


class URLService:
    def __init__(self, repository: URLRepository):
        self.repository = repository

    def generate_short_code(self) -> str:
        """
        Generate a random URL-safe short code.
        """
        return secrets.token_urlsafe(SHORT_CODE_BYTES)

    def short_code_exists(self, short_code: str) -> bool:
        """
        Check whether a short code already exists in the database.
        """
        return self.repository.get_by_short_code(short_code) is not None

    def generate_unique_short_code(self) -> str:
        """
        Generate a unique short code.

        Retry up to MAX_RETRY_ATTEMPTS times before failing.
        """
        for _ in range(MAX_RETRY_ATTEMPTS):
            short_code = self.generate_short_code()

            if not self.short_code_exists(short_code):
                return short_code

        raise RuntimeError(
            f"Failed to generate a unique short code after "
            f"{MAX_RETRY_ATTEMPTS} attempts."
        )

    def create_short_url(self, original_url: str) -> URL:
        """
        Create and persist a new shortened URL.
        """
        short_code = self.generate_unique_short_code()

        url = URL(
            original_url=original_url,
            short_code=short_code,
        )

        return self.repository.create(url)

    # Retrieve the original URL based on the provided short code.
    def get_url_by_short_code(self, short_code: str) -> URL:
        url = self.repository.get_by_short_code(short_code)
        if not url:
            raise URLNotFoundException(short_code)
        return url