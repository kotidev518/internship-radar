import json
import logging
import google.generativeai as genai
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models import RawJob, Internship
from config.settings import settings
import asyncio

logger = logging.getLogger(__name__)

# Configure Gemini
if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)

generation_config = {
  "temperature": 0.2, # Low temp for deterministic structured output
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json", # Force JSON output
}

prompt_template = """
Extract structured internship information from the following job description.

Return JSON strictly matching this schema:
{{
 "role": "string",
 "skills": ["string"],
 "category": "string",
 "remote": boolean,
 "stipend": "string | null"
}}

Rules:
- Normalize the job title
- Extract only technical skills
- Category MUST be exactly one of: "Frontend", "Backend", "Full Stack", "AI/ML", "Mobile", "Data", "Other"
- Remote must be true or false (boolean)
- If stipend is not mentioned, return null. 

Job Title: {title}

Job Description: {description}
"""

class GeminiProcessor:
    def __init__(self):
        self.model = None
        if settings.gemini_api_key:
             self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config
            )

    async def process_batch(self):
        if not self.model:
            logger.error("Gemini API key not configured. Skipping extraction.")
            return

        logger.info(f"Starting Gemini batch processing. Batch size: {settings.batch_size}")
        db: Session = SessionLocal()
        
        try:
            # Fetch unprocessed jobs
            raw_jobs = db.query(RawJob).filter(RawJob.processed == False).limit(settings.batch_size).all()
            
            if not raw_jobs:
                logger.info("No unprocessed jobs found.")
                return

            for raw_job in raw_jobs:
                await self._process_single_job(db, raw_job)
                
        finally:
            db.close()
            
    async def _process_single_job(self, db: Session, raw_job: RawJob, retries=3):
        prompt = prompt_template.format(
            title=raw_job.title or "Unknown",
            description=raw_job.description or ""
        )
        
        for attempt in range(retries):
            try:
                response = self.model.generate_content(prompt)
                
                # Parse JSON
                structured_data = json.loads(response.text)
                
                # Validate Category
                category = structured_data.get("category", "Other")
                valid_categories = ["Frontend", "Backend", "Full Stack", "AI/ML", "Mobile", "Data", "Other"]
                if category not in valid_categories:
                    category = "Other"
                
                # Check for duplicate apply_link in internships table before saving
                existing_internship = db.query(Internship).filter(Internship.apply_link == raw_job.apply_link).first()
                if not existing_internship:
                    new_internship = Internship(
                        role=structured_data.get("role", raw_job.title),
                        company=raw_job.company,
                        location=raw_job.location,
                        skills=structured_data.get("skills", []),
                        category=category,
                        remote=bool(structured_data.get("remote", False)),
                        stipend=structured_data.get("stipend"),
                        apply_link=raw_job.apply_link,
                        source=raw_job.source
                    )
                    db.add(new_internship)
                
                # Mark raw job as processed (even if duplicate, we don't need to try again)
                raw_job.processed = True
                db.commit()
                logger.info(f"Successfully processed raw_job {raw_job.id}: {structured_data.get('role')}")
                break # Break out of retry loop on success
                
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON for raw_job {raw_job.id} on attempt {attempt+1}")
                if attempt == retries - 1:
                     # Mark processed so we don't get stuck in a loop of failures
                    raw_job.processed = True 
                    db.commit()
            except Exception as e:
                logger.error(f"Error processing raw_job {raw_job.id} on attempt {attempt+1}: {e}")
                if attempt == retries - 1:
                     raw_job.processed = True
                     db.commit()
            
            # Brief delay between retries
            await asyncio.sleep(2)
