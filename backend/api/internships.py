from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from database.connection import get_db
from database.models import Internship
from api.schemas import InternshipResponse
from scheduler.scheduler import scheduled_pipeline

router = APIRouter(prefix="/internships", tags=["Internships"])

@router.get("", response_model=List[InternshipResponse])
def get_internships(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all internships with pagination."""
    internships = db.query(Internship).order_by(Internship.created_at.desc()).offset(skip).limit(limit).all()
    return internships

@router.post("/scrape")
async def trigger_scraping(background_tasks: BackgroundTasks):
    """Trigger the master scraper and AI processing pipeline in the background."""
    background_tasks.add_task(scheduled_pipeline)
    return {"message": "Scraping and AI processing pipeline started in the background."}


@router.get("/search", response_model=List[InternshipResponse])
def search_internships(
    q: Optional[str] = None,
    role: Optional[str] = None,
    category: Optional[str] = None,
    remote: Optional[bool] = None,
    skills: Optional[str] = None, # comma-separated list
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Search and filter internships."""
    query = db.query(Internship)

    if q:
        search_filter = or_(
            Internship.role.ilike(f"%{q}%"),
            Internship.company.ilike(f"%{q}%")
        )
        query = query.filter(search_filter)

    if role:
        query = query.filter(Internship.role.ilike(f"%{role}%"))
    
    if category:
        query = query.filter(Internship.category == category)
        
    if remote is not None:
        query = query.filter(Internship.remote == remote)
        
    if skills:
        skill_list = [s.strip() for s in skills.split(',')]
        # PostgreSQL specific array containment
        query = query.filter(Internship.skills.contains(skill_list))

    internships = query.order_by(Internship.created_at.desc()).offset(skip).limit(limit).all()
    return internships
