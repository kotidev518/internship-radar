# Tech Stack

## Frontend

Framework
Next.js

Language
TypeScript

Styling
Tailwind CSS

Component Library
ShadCN UI

Responsibilities

* internship dashboard
* search functionality
* internship tracker
* filtering by skills

Deployment
Vercel

---

## Backend

Runtime
Node.js

Framework
Next.js API Routes

Responsibilities

* serve internship data
* manage application tracker
* provide search endpoints

---

## Database

Database
Neon PostgreSQL

ORM
Prisma

Tables

raw_jobs
internships
applications

---

## Scraper System

Language
Python

Primary Scraper Tool

Playwright

Responsibilities

* open keyword search pages
* collect internship listings
* extract raw job data
* insert records into raw_jobs table

---

## AI Preprocessing

AI Model

Gemini 1.5 Flash

Responsibilities

* normalize job titles
* extract skills
* detect internship category
* detect remote roles

---

## Pipeline Architecture

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

## Hosting

Frontend
Vercel

Database
Neon PostgreSQL

Scraper Workers
GitHub Actions scheduled jobs

---

## Environment Variables

DATABASE_URL
GEMINI_API_KEY
SCRAPER_INTERVAL
