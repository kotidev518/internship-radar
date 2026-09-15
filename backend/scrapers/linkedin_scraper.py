import asyncio
import logging
from urllib.parse import urljoin
from scrapers.base_scraper import BaseScraper, KEYWORDS
from database.connection import SessionLocal
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

class LinkedinScraper(BaseScraper):
    """Scraper for LinkedIn Jobs search results."""
    
    def __init__(self):
        super().__init__(source_name="LinkedIn")
    
    async def scrape(self):
        logger.info(f"Starting {self.source_name} scraper...")
        db = SessionLocal()
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=self.get_random_user_agent())
                page = await context.new_page()

                for keyword in KEYWORDS:
                    formatted_kw = keyword.replace(" ", "%20")
                    search_url = f"https://www.linkedin.com/jobs/search/?keywords={formatted_kw}&f_E=1"
                    
                    await self.add_delay()
                    logger.info(f"[{self.source_name}] Scraping keyword: {keyword} -> {search_url}")
                    
                    try:
                        await page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
                        await page.wait_for_timeout(1000)
                        cards = await page.query_selector_all(".base-card, .job-search-card, li")
                        for card in cards:
                            title = await card.query_selector(".base-search-card__title")
                            company = await card.query_selector(".base-search-card__subtitle")
                            location = await card.query_selector(".job-search-card__location")
                            link_el = await card.query_selector("a.base-card__full-link, a")
                            href = await link_el.get_attribute("href") if link_el else None
                            if title and href:
                                self.save_raw_job(db, {
                                    "title": (await title.inner_text()).strip(),
                                    "company": (await company.inner_text()).strip() if company else "",
                                    "location": (await location.inner_text()).strip() if location else "",
                                    "description": "",
                                    "apply_link": urljoin("https://www.linkedin.com", href.strip()),
                                })
                    except Exception as e:
                        logger.error(f"Error scraping {search_url}: {e}")
                        
                await browser.close()
        finally:
            db.close()
        logger.info(f"Finished {self.source_name} scraper.")
