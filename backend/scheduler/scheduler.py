import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from scrapers.run_scrapers import run_all_scrapers
from services.gemini_processor import GeminiProcessor

logger = logging.getLogger(__name__)

async def scheduled_pipeline():
    logger.info("--- Starting Scheduled Job Pipeline ---")
    
    # Run scrapers (Step 1)
    await run_all_scrapers()
    
    # Run AI Processor (Step 2)
    processor = GeminiProcessor()
    await processor.process_batch()
    
    logger.info("--- Finished Scheduled Job Pipeline ---")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    
    # Run twice daily (09:00 and 18:00)
    scheduler.add_job(
        scheduled_pipeline, 
        CronTrigger(hour=9, minute=0), 
        id="morning_scrape"
    )
    scheduler.add_job(
        scheduled_pipeline, 
        CronTrigger(hour=18, minute=0), 
        id="evening_scrape"
    )
    
    scheduler.start()
    logger.info("APScheduler started (Jobs at 09:00, 18:00).")
    return scheduler

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_scheduler()
    asyncio.get_event_loop().run_forever()
