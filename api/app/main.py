from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from .schemas import URLRequest, URLResponse, HealthCheckResponse
from .services.url_service import URLService
from .database import get_db
from .repositories.url_repository import URLRepository
from .config import settings
from .exceptions import URLNotFoundException, url_not_found_exception_handler
import logging
from .logging import get_logger
from sqlalchemy import text

logger = get_logger(__name__)
app = FastAPI()
app.add_exception_handler(URLNotFoundException, url_not_found_exception_handler)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")

# Add health check endpoint
@app.get("/health", response_model=HealthCheckResponse)

def health_check(db: Session = Depends(get_db)):
    """
    Verifies application health and PostgreSQL connectivity.
    Returns HTTP 503 if the database is unreachable.
    """
    try:
        # Attempt to execute a simple query to check database connectivity
        db.execute(text("SELECT 1"))
        return HealthCheckResponse(status="healthy", database="connected")
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
   

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
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
    
        url_record = url_service.get_url_by_short_code(short_code)
        return RedirectResponse(
            url=url_record.original_url,
            status_code=status.HTTP_302_FOUND
        )
    