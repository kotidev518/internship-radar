from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

# Common
class InternshipBase(BaseModel):
    role: str
    company: str
    location: str
    skills: List[str]
    category: str
    remote: bool
    stipend: Optional[str] = None
    apply_link: str
    source: str

class InternshipResponse(InternshipBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ApplicationBase(BaseModel):
    internship_id: int
    status: str = "saved"
    notes: Optional[str] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationResponse(ApplicationBase):
    id: int
    applied_date: Optional[datetime] = None
    updated_at: datetime
    internship: InternshipResponse
    
    class Config:
        from_attributes = True

class ApplicationStatusUpdate(BaseModel):
    status: str # saved, applied, interview, rejected, offer
