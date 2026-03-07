import asyncio
import logging
from scrapers.internshala_scraper import InternshalaScraper
from scrapers.linkedin_scraper import LinkedinScraper
from scrapers.wellfound_scraper import WellfoundScraper
from scrapers.indeed_scraper import IndeedScraper
from scrapers.company_pages_scraper import CompanyPagesScraper

logger = logging.getLogger(__name__)

async def run_all_scrapers():
    """Master scraper coordinator. Runs all scrapers sequentially."""
    logger.info("========== Starting Master Scraper Runner ==========")
    
    scrapers = [
        InternshalaScraper(),
        LinkedinScraper(),
        WellfoundScraper(),
        IndeedScraper(),
        CompanyPagesScraper(),
    ]
    
    results = {}
    for scraper in scrapers:
        try:
            await scraper.scrape()
            results[scraper.source_name] = "success"
        except Exception as e:
            logger.error(f"Error running scraper {scraper.source_name}: {e}")
            results[scraper.source_name] = f"failed: {e}"
    
    logger.info(f"========== Scraper Results: {results} ==========")
    return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_all_scrapers())
