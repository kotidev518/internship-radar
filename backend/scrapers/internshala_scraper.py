import asyncio
import logging
from scrapers.base_scraper import BaseScraper, KEYWORDS
from database.connection import SessionLocal
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

class InternshalaScraper(BaseScraper):
    def __init__(self):
        super().__init__(source_name="Internshala")
    
    async def scrape(self):
        logger.info(f"Starting {self.source_name} scraper...")
        db = SessionLocal()
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(user_agent=self.get_random_user_agent())
                page = await context.new_page()
                
                for keyword in KEYWORDS:
                    formatted_kw = keyword.replace(" ", "-") # e.g. "react-internship"
                    search_url = f"https://internshala.com/internships/{formatted_kw}"
                    
                    await self.add_delay()
                    logger.info(f"[{self.source_name}] Scraping keyword: {keyword} -> {search_url}")
                    
                    try:
                        await page.goto(search_url, wait_until="networkidle")
                        cards = await page.query_selector_all(".individual_internship")
                        for card in cards:
                            title_el = await card.query_selector(".heading_4_5.profile")
                            company_el = await card.query_selector(".heading_6.company_name")
                            location_el = await card.query_selector(".location_link")
                            link_el = await card.query_selector(".heading_4_5.profile a")
                            
                            if title_el and link_el:
                                href = await link_el.get_attribute("href")
                                self.save_raw_job(db, {
                                    "title": (await title_el.inner_text()).strip(),
                                    "company": (await company_el.inner_text()).strip() if company_el else "",
                                    "location": (await location_el.inner_text()).strip() if location_el else "",
                                    "description": "",
                                    "apply_link": f"https://internshala.com{href}" if href else "",
                                })
                    except Exception as e:
                        logger.error(f"Error scraping {search_url}: {e}")
                        
                await browser.close()
        finally:
            db.close()
        logger.info(f"Finished {self.source_name} scraper.")
