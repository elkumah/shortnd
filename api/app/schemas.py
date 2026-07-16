from pydantic import BaseModel
from pydantic import HttpUrl

# Define a Pydantic model for the request body
class URLRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    short_code: str
    shortened_url: str

# Define a Pydantic model for the request response when retrieving the original URL
class OriginalURLResponse(BaseModel):
    short_code: str
    original_url: HttpUrl