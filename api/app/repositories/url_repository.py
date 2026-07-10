from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models import URL

class URLRepository:
    def __init__(self, db: Session):
        self.db = db
    def create(self,url: URL) -> URL:
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)
        return url

    def get_by_short_code(self, short_code: str) -> Optional[URL]:
        # Retrieve a URL mapping from the database based on the provided short code.
        statement = select(URL).where(URL.short_code == short_code)
        result = self.db.execute(statement)
        return result.scalar_one_or_none()

    def exists_by_short_code(short_code: str) -> bool:
        # Check if a URL mapping with the given short code exists in the database.
        statement = select(URL).where(URL.short_code == short_code)
        result = self.db.execute(statement)
        return result.scalar_one_or_none() is not None