# Scraper Strategy

## Overview

This document defines the scraping architecture for the Internship Radar system.

The goal is to collect internship listings from multiple sources safely and efficiently while avoiding rate limits or bot detection.

The system uses a **multi-source scraping strategy**, where each website is scraped lightly instead of relying heavily on a single source.

This approach improves reliability and increases the number of internships collected per day.

---

# Data Pipeline

The internship data pipeline follows this architecture:

Multiple Job Sources
↓
Keyword Search Pages
↓
Playwright Scrapers
↓
Raw Job Data
↓
Gemini AI Processing
↓
Neon PostgreSQL
↓
Next.js Dashboard

---

# Multi-Source Scraping Strategy

Instead of scraping a single website aggressively, the system distributes requests across multiple platforms.

Example sources include:

Internshala
Wellfound
LinkedIn Jobs
Indeed
Startup career pages

Expected internships collected per day:

| Source               | Estimated Internships |
| -------------------- | --------------------- |
| Internshala          | 80–120                |
| LinkedIn             | 80–120                |
| Indeed               | 60–100                |
| Wellfound            | 50–80                 |
| Company career pages | 40–80                 |

Total estimated internships collected daily:

300–500 internships

---

# Scraper Modules

Each website is handled by its own scraper module.

This ensures the scraping logic for each source remains isolated and easy to maintain.

Example structure:

/scrapers
internshala_scraper.py
linkedin_scraper.py
wellfound_scraper.py
indeed_scraper.py
company_pages_scraper.py

Each module contains:

• page navigation logic
• HTML extraction logic
• data normalization logic

---

# Master Scraper Script

A master script coordinates all scrapers.

File:

run_scrapers.py

Example execution logic:

```python
from scrapers.internshala import scrape_internshala
from scrapers.linkedin import scrape_linkedin
from scrapers.wellfound import scrape_wellfound
from scrapers.indeed import scrape_indeed
from scrapers.company_pages import scrape_company_pages

scrape_internshala()
scrape_linkedin()
scrape_wellfound()
scrape_indeed()
scrape_company_pages()
```

Scrapers run sequentially to minimize load on target websites.

---

# Scraper Tool

The system uses:

Playwright

Playwright is chosen because many job platforms render listings using JavaScript.

Headless browsers allow the scraper to capture dynamic content.

---

# Keyword-Based Scraping

Internships are discovered through keyword search pages.

Example keywords:

react internship
full stack internship
ai internship
machine learning internship
frontend internship
backend internship

Example keyword list:

```python
keywords = [
 "react",
 "full stack",
 "ai",
 "machine learning",
 "frontend",
 "backend"
]
```

These keywords are used to generate search result pages.

Example search URLs:

internshala.com/internships/react-internship
internshala.com/internships/machine-learning-internship

Scraping search result pages ensures efficient discovery of relevant internships.

---

# Rate Limiting

Websites may block scrapers that send requests too quickly.

To avoid detection, the scraper introduces random delays between requests.

Example implementation:

```python
import time
import random

time.sleep(random.uniform(2,5))
```

This simulates natural browsing behavior.

---

# User-Agent Rotation

Many websites detect automated tools through the browser user-agent.

The scraper rotates user-agent headers to mimic different browsers.

Example:

```python
USER_AGENTS = [
 "Mozilla/5.0 Chrome/120",
 "Mozilla/5.0 Safari/537",
 "Mozilla/5.0 Firefox/118"
]
```

Playwright example:

```python
browser.new_context(user_agent=random.choice(USER_AGENTS))
```

---

# Google Index Scraping

Some internships appear in search engines before being discovered through normal scraping.

Google indexed pages can be used to discover hidden job listings.

Example search queries:

site:internshala.com "React Intern"
site:wellfound.com "Machine Learning Intern"

Links extracted from these results are then scraped directly.

---

# Company Career Page Scraping

Many startups publish internships only on their career pages.

Examples:

careers.razorpay.com
careers.zoho.com
jobs.swiggy.com

These pages provide additional internship opportunities not found on major job boards.

---

# Deduplication Strategy

Many internships appear across multiple job websites.

Duplicate records must be removed before storing the final internship data.

The system uses the application link as a unique identifier.

Example SQL insertion rule:

```sql
INSERT INTO internships (...)
ON CONFLICT (apply_link) DO NOTHING;
```

This ensures duplicate listings are automatically ignored.

---

# Safe Request Volume

A safe scraping rate is maintained to avoid being blocked.

Recommended request speed:

2–5 seconds per request

Typical scraping volume:

50 requests per website
× 5 websites

Total:

250 requests per scraping cycle

---

# Scraper Execution Schedule

Scrapers run twice daily.

Schedule:

09:00 AM
06:00 PM

Execution flow:

Scraper → Raw Job Data → Gemini preprocessing → Clean internship records

---

# Raw Job Data

Scrapers insert collected data into the raw_jobs table.

Example fields:

title
company
location
description
apply_link
source

These records are later processed by the AI pipeline.

---

# AI Processing

Raw job descriptions are sent to Gemini AI for preprocessing.

AI extracts structured fields including:

role
skills
category
remote status
stipend

Clean internship records are then inserted into the internships table.

---

# Expected Daily Output

Typical daily internship collection:

Internshala → 110
LinkedIn → 95
Wellfound → 70
Indeed → 90
Company pages → 60

Estimated total:

≈ 425 internships per day

---

# Project Folder Structure

Recommended project structure:

project
│
├─ scraper
│   ├─ internshala_scraper.py
│   ├─ linkedin_scraper.py
│   ├─ wellfound_scraper.py
│   ├─ indeed_scraper.py
│   └─ run_scrapers.py
│
├─ ai_processing
│   └─ gemini_processor.py
│
├─ database
│   └─ db_client.py
│
├─ api
│   └─ nextjs_backend
│
└─ frontend
└─ dashboard

---

# Reliability Considerations

To ensure stable scraping:

• maintain rate limits
• rotate user agents
• distribute scraping across sources
• remove duplicate records
• store raw job data for debugging

---

# Summary

The scraping system combines:

• multi-source scraping
• keyword-based discovery
• headless browser automation
• AI data preprocessing

This architecture enables reliable collection of **300–500 internships per day** while minimizing the risk of blocking or detection.

Responsible Scraping Guidelines

• Scrape only publicly accessible pages
• Do not scrape behind login authentication
• Respect robots.txt directives
• Maintain request delays between 2–5 seconds
• Link users to the original job posting
• Avoid storing full copyrighted job descriptions
