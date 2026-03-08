import pytest
from unittest.mock import MagicMock, AsyncMock
from scrapers.internshala_scraper import InternshalaScraper

@pytest.mark.asyncio
async def test_internshala_scraper(mocker):
    scraper = InternshalaScraper()
    
    # Mock the database session
    mock_session = MagicMock()
    mocker.patch("scrapers.internshala_scraper.SessionLocal", return_value=mock_session)
    
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
    
    mock_title.inner_text.return_value = "React Intern"
    mock_company.inner_text.return_value = "Tech Corp"
    mock_location.inner_text.return_value = "Remote"
    mock_link.get_attribute.return_value = "/internship/react"
    
    # When query_selector_all is called, return one mock card
    mock_page.query_selector_all.return_value = [mock_card]
    
    # Card element lookups
    mock_card.query_selector.side_effect = lambda selector: {
        ".heading_4_5.profile": mock_title,
        ".heading_6.company_name": mock_company,
        ".location_link": mock_location,
        ".heading_4_5.profile a": mock_link,
    }.get(selector, None)
    
    # Connect playwright mocks
    mock_context.new_page.return_value = mock_page
    mock_browser.new_context.return_value = mock_context
    mock_playwright.chromium.launch.return_value = mock_browser
    
    # Create an async context manager mock for playwright
    p_context_manager = AsyncMock()
    p_context_manager.__aenter__.return_value = mock_playwright
    
    mocker.patch("scrapers.internshala_scraper.async_playwright", return_value=p_context_manager)
    
    # Mock KEYWORDS so we only loop once
    mocker.patch("scrapers.internshala_scraper.KEYWORDS", ["react internship"])
    
    # Spy on save_raw_job to ensure it's called
    spy_save_raw_job = mocker.spy(scraper, "save_raw_job")
    
    # Mock delay to speed up tests
    mocker.patch.object(scraper, "add_delay", new_callable=AsyncMock)
    
    # Run the scrape method
    await scraper.scrape()
    
    # Verify save_raw_job was called with the correct extracted data
    spy_save_raw_job.assert_called()
    call_args = spy_save_raw_job.call_args[0]
    job_data = call_args[1]
    
    assert job_data["title"] == "React Intern"
    assert job_data["company"] == "Tech Corp"
    assert job_data["location"] == "Remote"
    assert job_data["apply_link"] == "https://internshala.com/internship/react"
