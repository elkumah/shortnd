from fastapi import Request, status
from fastapi.responses import JSONResponse
from .custom_exceptions import URLNotFoundException

async def url_not_found_exception_handler(request: Request, exc: URLNotFoundException):
    """
    Handle URLNotFoundException and return a JSON response with error details.
    """
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
    