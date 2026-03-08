import pytest
from unittest.mock import MagicMock, AsyncMock
from scrapers.indeed_scraper import IndeedScraper

@pytest.mark.asyncio
async def test_indeed_scraper(mocker):
    scraper = IndeedScraper()
    
    # Mock the database session
    mock_session = MagicMock()
    mocker.patch("scrapers.indeed_scraper.SessionLocal", return_value=mock_session)
    
    # Mock playwright
    mock_playwright = AsyncMock()
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    
    # Mock page context and elements
    mock_card = AsyncMock()
    mock_title = AsyncMock()
    mock_company = AsyncMock()
    mock_location = AsyncMock()
    mock_link = AsyncMock()
    
    mock_title.inner_text.return_value = "Python Dev"
    mock_company.inner_text.return_value = "Great Place"
    mock_location.inner_text.return_value = "New York"
    mock_link.get_attribute.return_value = "/viewjob?jk=123"
    
    mock_page.query_selector_all.return_value = [mock_card]
    
    mock_card.query_selector.side_effect = lambda selector: {
        "h2.jobTitle span": mock_title,
        "[data-testid='company-name']": mock_company,
        "[data-testid='text-location']": mock_location,
        "h2.jobTitle a": mock_link,
    }.get(selector, None)
    
    # Connect playwright mocks
    mock_context.new_page.return_value = mock_page
    mock_browser.new_context.return_value = mock_context
    mock_playwright.chromium.launch.return_value = mock_browser
    
    p_context_manager = AsyncMock()
    p_context_manager.__aenter__.return_value = mock_playwright
    
    mocker.patch("scrapers.indeed_scraper.async_playwright", return_value=p_context_manager)
    mocker.patch("scrapers.indeed_scraper.KEYWORDS", ["python internship"])
    
    spy_save_raw_job = mocker.spy(scraper, "save_raw_job")
    mocker.patch.object(scraper, "add_delay", new_callable=AsyncMock)
    
    await scraper.scrape()
    
    spy_save_raw_job.assert_called()
    call_args = spy_save_raw_job.call_args[0]
    job_data = call_args[1]
    
    assert job_data["title"] == "Python Dev"
    assert job_data["company"] == "Great Place"
    assert job_data["location"] == "New York"
    assert job_data["apply_link"] == "https://www.indeed.com/viewjob?jk=123"
