import secrets
class URLService:
    def generate_short_code(self, url: str) -> str:
# The URL will be used later when checking for duplicate URLs and storing mappings in PostgreSQL.
        # Generate a cryptographically secure URL-safe short code.
        SHORT_CODE_BYTE = 6  # Length of the short code
        short_code = secrets.token_urlsafe(SHORT_CODE_BYTE) 
        return short_code