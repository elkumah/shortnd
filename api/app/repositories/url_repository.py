
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..logging.logger import get_logger
from ..models import URL

logger = get_logger(__name__)

class URLRepository:
    def __init__(self, db: Session):
        self.db = db
    def create(self,url: URL) -> URL:
        # add logging for creating a new URL mapping
        logger.info(f"Creating a new URL mapping for: {url.original_url}")
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    def get_by_short_code(self, short_code: str) -> URL | None:
        # add logging for retrieving a URL mapping by short code
        logger.info(f"Retrieving URL mapping for short code: {short_code}")
        # Retrieve a URL mapping from the database based on the provided short code.
        statement = select(URL).where(URL.short_code == short_code)
        result = self.db.execute(statement)
        return result.scalar_one_or_none()

    def exists_by_short_code(self, short_code: str) -> bool:
        # add logging for checking existence of a URL mapping by short code
        logger.info(f"Checking existence of URL mapping for short code: {short_code}")
        # Check if a URL mapping with the given short code exists in the database.
        statement = select(URL).where(URL.short_code == short_code)
        result = self.db.execute(statement)
        return result.scalar_one_or_none() is not None