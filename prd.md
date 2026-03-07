# Product Requirements Document

## Product Name

Internship Radar

## Overview

Internship Radar is a personal internship discovery and tracking system that aggregates internship opportunities from multiple job sources, processes them using AI, and displays them in a searchable dashboard.

The system uses a multi-source scraping strategy combined with AI preprocessing to build a clean database of internship opportunities.

---

# Core Workflow

The platform follows this data pipeline:

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

# Objectives

1. Aggregate internships from multiple job platforms.
2. Use keyword-based search scraping to discover opportunities.
3. Process raw job descriptions using AI to extract structured data.
4. Provide a clean and searchable internship dashboard.
5. Allow tracking internship application status.

---

# Internship Data Sources

The scraper collects internships from multiple platforms including:

* LinkedIn Jobs
* Internshala
* Wellfound
* Indeed
* Startup career pages

Each source is accessed through keyword search pages to maximize coverage.

Example keywords:

* React internship
* Full stack internship
* AI internship
* Machine learning internship
* Frontend internship
* Backend internship

---

# Data Extraction

The Playwright scraper collects raw job fields including:

* job title
* company name
* location
* job description
* application link
* source platform

These records are stored as raw job data.

---

# AI Data Processing

Raw job descriptions are sent to Gemini AI for preprocessing.

The AI extracts structured information:

* normalized role title
* skills
* internship category
* remote status
* stipend (if available)

The cleaned internship record is then stored in the database.

---

# Internship Dashboard

The dashboard displays processed internship records.

Each internship card includes:

* role
* company
* location
* skills
* category
* application link
* source website

Users can search internships using keywords.

---

# Application Tracker

The system includes a personal internship tracker.

Statuses:

Saved
Applied
Interview
Rejected
Offer

This enables the dashboard to function as a personal internship CRM.

---

# Scraper Schedule

Scrapers run twice per day:

09:00 AM
06:00 PM

This keeps internship data fresh while minimizing system load.

---

# MVP Scope

Initial release includes:

* multi-source internship scraping
* keyword search scraping
* AI preprocessing
* internship dashboard
* application tracking
