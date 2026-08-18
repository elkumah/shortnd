
from fastapi import Request, status
from fastapi.responses import JSONResponse

from ..logging.logger import get_logger
from .custom_exceptions import URLNotFoundException

logger = get_logger(__name__)

async def url_not_found_exception_handler(request: Request, exc: URLNotFoundException):
    """
    Handle URLNotFoundException and return a JSON response with error details.
    Logs the error and returns a JSON response with a 404 status code.
    """
    logger.error(f"URL not found: {exc.short_code}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "success": False,
            "error": {
                "code": "URL_NOT_FOUND",
                "message": str(exc),
                "short_code": exc.short_code
            }
        }
    )
    