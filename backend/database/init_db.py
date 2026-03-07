from database.connection import engine
from database.models import Base
import logging

logger = logging.getLogger(__name__)

def init_database():
    try:
        if engine:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully (if they didn't exist).")
        else:
            logger.error("Engine not found. Cannot initialize DB.")
    except Exception as e:
        logger.error(f"Error initializing DB: {e}")

if __name__ == "__main__":
    init_database()
