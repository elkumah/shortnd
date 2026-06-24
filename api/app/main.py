from fastapi import FastAPI
from .schemas import URLRequest
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World. Testing Fast API endpoint."}

@app.post("/shorten/")
async def shorten_url(url_request: URLRequest):
    url = url_request.url
    return {"short_code": "abc123",  "shortened_url": f"http://short.ly/abc123"}
