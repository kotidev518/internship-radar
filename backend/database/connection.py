from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

# To test properly, the engine shouldn't be created globally just in case DATABASE_URL is bad during tests, but for simplicity we can do it.
try:
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"Error creating database engine: {e}")
    # Still define things so imports don't fail immediately, even if connection string is dummy
    engine = None
    SessionLocal = None

def get_db():
    if not SessionLocal:
        raise Exception("Database session factory is not initialized. Check your DATABASE_URL.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
