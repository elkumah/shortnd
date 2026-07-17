from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .schemas import URLRequest, URLResponse
from .services.url_service import URLService
from .database import get_db
from .repositories.url_repository import URLRepository
from .config import settings

app = FastAPI()


@app.get("/")
def root():
    return {
    "message": "Secure URL Shortener API",
    "version": "1.0.0"
}

def get_url_service(db: Session = Depends(get_db)) -> URLService:
    """
    Create and return a URLService instance for each request.
    """
    url_repository = URLRepository(db)
    # Create and return a URLService instance using the URLRepository
    return URLService(url_repository)

@app.post("/shorten/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def shorten_url( url_request: URLRequest,url_service: URLService = Depends(get_url_service)):
    url_record = url_service.create_short_url(str(url_request.url))

    return URLResponse(
        short_code=url_record.short_code,
        shortened_url=f"{settings.BASE_URL}/{url_record.short_code}"
    )
    
# Return redirect response to the original URL based on the provided short code.

@app.get("/{short_code}")
async def redirect_to_original_url(short_code: str, url_service: URLService = Depends(get_url_service)):
    try:
        url_record = url_service.get_url_by_short_code(short_code)
        return RedirectResponse(
            url=url_record.original_url,
            status_code=status.HTTP_302_FOUND
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No URL found for short code: {short_code}"
        )