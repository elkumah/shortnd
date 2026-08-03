import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

TEST_DATABASE_URL = (
        "postgresql://shortnd:shortnd@localhost:5432/shortnd_test"
)

engine = create_engine(
    TEST_DATABASE_URL
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
@pytest.fixture(scope="session", autouse=True)
def create_test_database():

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)



@pytest.fixture
def db_session():

    session = TestingSessionLocal()

    try:
        yield session

    finally:
        session.rollback()
        session.close()