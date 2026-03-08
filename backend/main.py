from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.init_db import init_database
from config.settings import settings
from api import internships, applications
import logging
from config.logging_config import setup_logging
from fastapi import BackgroundTasks
from scheduler.scheduler import scheduled_pipeline

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Internship Radar API", description="Backend for the Internship Radar Next.js Dashboard")

# Initialize database and scheduler
@app.on_event("startup")
async def startup_event():
    init_database()
    from scheduler.scheduler import start_scheduler
    start_scheduler()

# Set up CORS for Next.js frontend
origins = [settings.frontend_url, "http://localhost:3000"]
if settings.frontend_url != "http://localhost:3000":
    origins.append("http://localhost:3000") # Ensure local dev still works

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(internships.router, prefix="/api")
app.include_router(applications.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Internship Radar API", "docs": "/docs"}

@app.post("/api/trigger-scrape")
async def trigger_scrape_endpoint(background_tasks: BackgroundTasks):
    """
    Endpoint to manually trigger the scraping pipeline.
    Useful for triggering from external cron jobs (like GitHub Actions)
    if the Hugging Face Space was asleep during the normal schedule.
    """
    background_tasks.add_task(scheduled_pipeline)
    return {"message": "Scraping pipeline triggered in the background"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
