---
title: Internship Radar
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Internship Radar

Automated internship and job scraper with AI processing.

## Real-Time Scraping & Deployment Troubleshooting

If you encounter a **"Failed to start scrape"** alert or real-time scraping fails to display new internships on the deployed production site (e.g. Vercel), consider the following root causes and remedies:

### 1. Frontend Environment Variable (`NEXT_PUBLIC_API_URL`)
* **Issue:** By default, `frontend/src/lib/api.ts` falls back to `http://localhost:8000/api`. When deployed on Vercel, browser requests to `http://localhost:8000` fail because the browser cannot connect to your local machine, resulting in network/CORS errors and showing `"Failed to start scrape"`.
* **Fix:** Set `NEXT_PUBLIC_API_URL` in your Vercel Project Environment Settings to point to your live backend URL (e.g., `https://your-backend-api.onrender.com/api` or `https://your-space.hf.space/api`).

### 2. Backend Environment Variable (`FRONTEND_URL`)
* **Issue:** Fast API CORS middleware rejects requests from unknown origins.
* **Fix:** Set `FRONTEND_URL` in your backend environment variables to match your Vercel URL (e.g. `https://internship-radar.vercel.app`).

### 3. Playwright & Browser Dependencies on Cloud Hosting
* **Issue:** Playwright scrapers require Chromium binaries and system libraries (`playwright install --with-deps chromium`). Serverless functions (like Vercel API routes or AWS Lambda) or minimal container environments do not include headless browser dependencies by default.
* **Fix:** Deploy the Python backend on a Docker container environment (e.g., Render Docker Web Service, Hugging Face Docker Space, or AWS ECS) using the provided `Dockerfile` that includes Playwright dependencies.

### 4. Background AI Processing Pipeline
* **Issue:** Scraping saves entries to `raw_jobs`. The frontend displays items from `internships` (which requires Gemini AI processing).
* **Fix:** Ensure `GEMINI_API_KEY` and `DATABASE_URL` are configured properly in backend environment variables. The built-in fallback heuristic processor will automatically format records if Gemini credentials are not present.
