from pydantic import BaseModel, Field, HttpUrl


# Define a Pydantic model for the request body
class URLRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    short_code: str = Field(
        min_length=6,
        max_length=20,
    )
    shortened_url: str

# Define a Pydantic model for the request response when retrieving the original URL
class OriginalURLResponse(BaseModel):
    short_code: str = Field(
        min_length=6,
        max_length=20,
    )
    original_url: HttpUrl

# Define health check response model
class HealthCheckResponse(BaseModel):
    status: str
    database: str 