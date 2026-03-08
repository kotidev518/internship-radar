import pytest
import asyncio
from scrapers.base_scraper import BaseScraper, USER_AGENTS
from unittest.mock import MagicMock, AsyncMock

class DummyScraper(BaseScraper):
    async def scrape(self):
        pass

def test_get_random_user_agent():
    scraper = DummyScraper("Dummy")
    agent = scraper.get_random_user_agent()
    assert agent in USER_AGENTS

@pytest.mark.asyncio
async def test_add_delay(mocker):
    scraper = DummyScraper("Dummy")
    mock_sleep = mocker.patch("asyncio.sleep", new_callable=AsyncMock)
    await scraper.add_delay(1.0, 1.0)
    mock_sleep.assert_called_once_with(1.0)

def test_save_raw_job_new(mocker):
    scraper = DummyScraper("Dummy")
    mock_db = MagicMock()
    
    # Mock existing job as None (not found)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    job_data = {
        "title": "Software Engineer Intern",
        "company": "Tech Corp",
        "location": "Remote",
        "description": "Great role",
        "apply_link": "https://example.com/apply",
    }
    
    scraper.save_raw_job(mock_db, job_data)
    
    # New job should be added and committed
    assert mock_db.add.called
    assert mock_db.commit.called

def test_save_raw_job_duplicate(mocker):
    scraper = DummyScraper("Dummy")
    mock_db = MagicMock()
    
    # Mock existing job as Truthy (found)
    mock_db.query.return_value.filter.return_value.first.return_value = MagicMock()
    
    job_data = {
        "apply_link": "https://example.com/apply",
    }
    
    scraper.save_raw_job(mock_db, job_data)
    
    # Nothing should be added
    assert not mock_db.add.called
    assert not mock_db.commit.called

def test_save_raw_job_no_link(mocker):
    scraper = DummyScraper("Dummy")
    mock_db = MagicMock()
    
    job_data = {
        "title": "No Link Job",
    }
    
    scraper.save_raw_job(mock_db, job_data)
    assert not mock_db.add.called
