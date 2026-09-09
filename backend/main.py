from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from database.init_db import init_database
from config.settings import settings
from api import internships, applications
import logging
from config.logging_config import setup_logging
from scheduler.scheduler import scheduled_pipeline, start_scheduler

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    scheduler = start_scheduler()
    yield
    if scheduler and scheduler.running:
        scheduler.shutdown()

app = FastAPI(
    title="Internship Radar API",
    description="Backend for the Internship Radar Next.js Dashboard",
    lifespan=lifespan
)

# Set up CORS for Next.js frontend
raw_origins = [settings.frontend_url, "http://localhost:3000", "http://127.0.0.1:3000"]
origins = list({origin.rstrip('/') for origin in raw_origins if origin})

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
