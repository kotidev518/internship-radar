from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class RawJob(Base):
    __tablename__ = "raw_jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    company = Column(Text)
    location = Column(Text)
    description = Column(Text)
    apply_link = Column(Text, unique=True, index=True)
    source = Column(Text)
    processed = Column(Boolean, default=False)
    scraped_at = Column(TIMESTAMP, server_default=func.now())

class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(Text, index=True)
    company = Column(Text)
    location = Column(Text)
    skills = Column(ARRAY(Text)) # Specific to PostgreSQL
    category = Column(Text, index=True)
    remote = Column(Boolean)
    stipend = Column(Text)
    apply_link = Column(Text, unique=True, index=True)
    source = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    applications = relationship("Application", back_populates="internship", cascade="all, delete-orphan")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    internship_id = Column(Integer, ForeignKey("internships.id", ondelete="CASCADE"))
    status = Column(Text, default="saved") # saved, applied, interview, rejected, offer
    notes = Column(Text)
    applied_date = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    internship = relationship("Internship", back_populates="applications")
