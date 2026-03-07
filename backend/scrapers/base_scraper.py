import asyncio
import random
import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import RawJob

logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"
]

KEYWORDS = [
    "react internship",
    "full stack internship",
    "ai internship",
    "machine learning internship",
    "frontend internship",
    "backend internship"
]

class BaseScraper:
    def __init__(self, source_name: str):
        self.source_name = source_name
    
    def get_random_user_agent(self) -> str:
        return random.choice(USER_AGENTS)
    
    async def add_delay(self, min_sec: float = 2.0, max_sec: float = 5.0):
        # Add random delay to prevent rate limiting
        delay = random.uniform(min_sec, max_sec)
        await asyncio.sleep(delay)
    
    def save_raw_job(self, db: Session, job_data: Dict[str, Any]):
        """
        Saves a raw job to the database if it doesn't already exist.
        """
        try:
            # Check for existing apply_link
            apply_link = job_data.get("apply_link")
            if not apply_link:
                return

            existing_job = db.query(RawJob).filter(RawJob.apply_link == apply_link).first()
            if existing_job:
                # Duplicate, skip
                return
            
            new_job = RawJob(
                title=job_data.get("title"),
                company=job_data.get("company"),
                location=job_data.get("location"),
                description=job_data.get("description"),
                apply_link=apply_link,
                source=self.source_name
            )
            db.add(new_job)
            db.commit()
            # logger.info(f"Saved new raw job from {self.source_name}: {new_job.title}")
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving raw job: {e}")

    async def scrape(self):
        """
        Abstract method. Should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement scrape()")
