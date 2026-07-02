class URLService:
    def generate_short_code(self, url: str) -> str:
       
        short_code = "xyz123"  # Replace this with your actual logic
        shortened_url = f"http://localhost:8000/{short_code}"
        return shortened_url