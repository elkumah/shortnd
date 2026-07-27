# Create URL not found exception handler
class URLNotFoundException(Exception):
    """
    Custom exception for handling cases where a URL is not found in the database.
    """
    def __init__(self, short_code: str):
        self.short_code = short_code
        self.message = f"No URL found for short code: {short_code}"
        super().__init__(self.message)
