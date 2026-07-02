from fastapi import FastAPI
from .schemas import URLRequest, URLResponse
from .services.url_service import URLService
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World. Testing Fast API endpoint."}


@app.post("/shorten/", response_model=URLResponse)
async def shorten_url(url_request: URLRequest):
    url = url_request.url
    url_service = URLService()
    shortened_url = url_service.generate_short_code(url)
    # Extract the short code from the shortened URL
    short_code = shortened_url.split("/")[-1]
    return URLResponse(short_code=short_code, shortened_url=shortened_url)