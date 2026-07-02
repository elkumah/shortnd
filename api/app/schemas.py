from pydantic import BaseModel
from pydantic import HttpUrl

# Define a Pydantic model for the request body
class URLRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    short_code: str
    shortened_url: str

