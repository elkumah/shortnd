from fastapi import FastAPI
from .schemas import URLRequest
from .schemas import URLResponse
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World. Testing Fast API endpoint."}

@app.post("/shorten/",response_model=URLResponse)
async def shorten_url(url_request: URLRequest):
    url = url_request.url
    return URLResponse(short_code="abc123", shortened_url=f"http://short.ly/abc123")
