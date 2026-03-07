# AI Build Tasks

The AI agent should implement the system following these phases.

---

# Phase 1 Project Setup

Create Next.js project with TypeScript.

Install:

TailwindCSS
ShadCN UI
Prisma

Create folders:

/app
/components
/scripts
/lib

---

# Phase 2 Database Setup

Connect to Neon PostgreSQL.

Create tables using schema.sql.

Run migrations.

Generate Prisma client.

---

# Phase 3 Multi Source Scraper

Create scraper modules for each job source.

Example structure:

/scrapers
internshala_scraper.py
linkedin_scraper.py
wellfound_scraper.py
indeed_scraper.py

Use Playwright to open keyword search pages.

Example keywords:

react internship
full stack internship
ai internship
machine learning internship

Extract raw job data and insert into raw_jobs table.

---

# Phase 4 AI Processing

Create AI processing worker.

Steps:

1. Read records from raw_jobs table.
2. Send job description to Gemini API.
3. Extract structured fields.
4. Insert clean record into internships table.

Ensure duplicate detection using apply_link.

---

# Phase 5 Backend API

Create API routes:

GET /api/internships
GET /api/internships/search
POST /api/application
PATCH /api/application/status

These routes power the dashboard and tracker.

---

# Phase 6 Dashboard UI

Create pages:

/dashboard
/tracker

Display internships as cards.

Add search bar and filters.

---

# Phase 7 Application Tracker

Implement status pipeline:

saved
applied
interview
rejected
offer

Allow updating internship status.

---

# Phase 8 Scheduling

Configure GitHub Actions cron job.

Run scraper twice daily.

09:00 AM
06:00 PM

Run AI preprocessing after scraping completes.

---

# Phase 9 Deployment

Deploy frontend to Vercel.

Connect Neon PostgreSQL.

Ensure scraper worker runs automatically.
