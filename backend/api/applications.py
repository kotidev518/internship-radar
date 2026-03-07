from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database.connection import get_db
from database.models import Application, Internship
from api.schemas import ApplicationCreate, ApplicationResponse, ApplicationStatusUpdate

router = APIRouter(prefix="/applications", tags=["Applications"])

VALID_STATUSES = ["saved", "applied", "interview", "rejected", "offer"]

@router.get("", response_model=List[ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    """Get all applications in the tracker."""
    return db.query(Application).all()

@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(app_create: ApplicationCreate, db: Session = Depends(get_db)):
    """Save an internship to the tracker."""
    # Verify internship exists
    internship = db.query(Internship).filter(Internship.id == app_create.internship_id).first()
    if not internship:
        raise HTTPException(status_code=404, detail="Internship not found")
        
    # Check if already applied/saved
    existing_app = db.query(Application).filter(Application.internship_id == app_create.internship_id).first()
    if existing_app:
        raise HTTPException(status_code=400, detail="Internship already tracked")
        
    if app_create.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {VALID_STATUSES}")

    new_app = Application(
        internship_id=app_create.internship_id,
        status=app_create.status,
        notes=app_create.notes,
        applied_date=datetime.utcnow() if app_create.status in ["applied", "interview", "offer", "rejected"] else None
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return new_app

@router.patch("/{app_id}/status", response_model=ApplicationResponse)
def update_application_status(app_id: int, status_update: ApplicationStatusUpdate, db: Session = Depends(get_db)):
    """Update application tracking status (for drag-and-drop Kanban)."""
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    if status_update.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {VALID_STATUSES}")

    app.status = status_update.status
    if status_update.status == "applied" and app.applied_date is None:
        app.applied_date = datetime.utcnow()
        
    db.commit()
    db.refresh(app)
    return app
