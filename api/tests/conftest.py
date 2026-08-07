import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.repositories.url_repository import URLRepository
from app.models import URL
from app.config import settings
from fastapi.testclient import TestClient

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
    session = TestingSessionLocal()
    session.query(URL).delete()  # Clear the URL table before each test
    session.commit()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def repository(db_session) -> URLRepository:
    """
    Create a URLRepository using the test database session.
    """
    return URLRepository(db_session)

@pytest.fixture
def client():
    return TestClient(app)