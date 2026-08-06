import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings

# Safety check to prevent running tests against the development database
assert "shortnd_test" in settings.DATABASE_URL, (
    "Tests must run against the test database."
)

# Create a SQLAlchemy engine using the test database
engine = create_engine(settings.DATABASE_URL)

# Create a session factory for tests
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db_session() -> Session:
    """
    Provide a database session to each test.

    After the test completes, roll back any uncommitted
    transaction and close the session.
    """
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()