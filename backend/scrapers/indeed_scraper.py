import asyncio
import logging
from urllib.parse import urljoin
from scrapers.base_scraper import BaseScraper, KEYWORDS
from database.connection import SessionLocal
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

class IndeedScraper(BaseScraper):
    """Scraper for Indeed job search results."""
    
    def __init__(self):
        super().__init__(source_name="Indeed")
    
    async def scrape(self):
        logger.info(f"Starting {self.source_name} scraper...")
        db = SessionLocal()
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=self.get_random_user_agent())
                page = await context.new_page()

                for keyword in KEYWORDS:
                    formatted_kw = keyword.replace(" ", "+")
                    search_url = f"https://www.indeed.com/jobs?q={formatted_kw}&sc=0kf%3Ajt(internship)%3B"
                    
                    await self.add_delay()
                    logger.info(f"[{self.source_name}] Scraping keyword: {keyword} -> {search_url}")

                    try:
                        await page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
                        await page.wait_for_timeout(1000)
                        cards = await page.query_selector_all(".job_seen_beacon")
                        for card in cards:
                            title_el = await card.query_selector("h2.jobTitle span")
                            company_el = await card.query_selector("[data-testid='company-name']")
                            location_el = await card.query_selector("[data-testid='text-location']")
                            link_el = await card.query_selector("h2.jobTitle a")
                            if title_el and link_el:
                                href = await link_el.get_attribute("href")
                                if href:
                                    self.save_raw_job(db, {
                                        "title": (await title_el.inner_text()).strip(),
                                        "company": (await company_el.inner_text()).strip() if company_el else "",
                                        "location": (await location_el.inner_text()).strip() if location_el else "",
                                        "description": "",
                                        "apply_link": urljoin("https://www.indeed.com", href.strip()),
                                    })
                    except Exception as e:
                        logger.error(f"Error scraping {search_url}: {e}")
                        
                await browser.close()
        finally:
            db.close()
        logger.info(f"Finished {self.source_name} scraper.")
