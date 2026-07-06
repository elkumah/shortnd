from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Import the instantiated config object from the config module
from .config import settings

engine = create_engine(settings.DATABASE_URL)
# Create session factory for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Define the base class for future database models to inherit from
Base = declarative_base()

# Create a function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()