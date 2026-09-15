import asyncio
import logging
from typing import List, Dict
from urllib.parse import urljoin
from scrapers.base_scraper import BaseScraper
from database.connection import SessionLocal
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

# Configurable list of startup career page URLs
COMPANY_CAREER_PAGES: List[Dict[str, str]] = [
    {"name": "Razorpay", "url": "https://razorpay.com/jobs/"},
    {"name": "Zoho", "url": "https://careers.zoho.com/jobs/"},
    {"name": "Swiggy", "url": "https://careers.swiggy.com/"},
    {"name": "Flipkart", "url": "https://www.flipkartcareers.com/"},
    {"name": "Freshworks", "url": "https://www.freshworks.com/company/careers/"},
]

class CompanyPagesScraper(BaseScraper):
    """Scraper for individual startup career pages."""
    
    def __init__(self):
        super().__init__(source_name="CompanyPages")
    
    async def scrape(self):
        logger.info(f"Starting {self.source_name} scraper...")
        db = SessionLocal()
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=self.get_random_user_agent())
                page = await context.new_page()

                for company in COMPANY_CAREER_PAGES:
                    await self.add_delay()
                    logger.info(f"[{self.source_name}] Scraping: {company['name']} -> {company['url']}")

                    try:
                        await page.goto(company["url"], wait_until="domcontentloaded", timeout=20000)
                        await page.wait_for_timeout(1000)
                        # Each company page has a different DOM structure
                        # Extract job cards by common patterns (h2/h3 with link)
                        links = await page.query_selector_all("a")
                        for link in links:
                            text = (await link.inner_text()).strip()
                            href = await link.get_attribute("href")
                            if "intern" in text.lower() and href:
                                self.save_raw_job(db, {
                                    "title": text,
                                    "company": company["name"],
                                    "location": "",
                                    "description": "",
                                    "apply_link": urljoin(company["url"], href.strip()),
                                })
                    except Exception as e:
                        logger.error(f"Error scraping {company['url']}: {e}")
                        
                await browser.close()
        finally:
            db.close()
        logger.info(f"Finished {self.source_name} scraper.")
