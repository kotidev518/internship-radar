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
            
    def _parse_gemini_response(self, text: str) -> dict:
        cleaned = text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        elif cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        return json.loads(cleaned.strip())

    def _fallback_process(self, raw_job: RawJob) -> dict:
        title = raw_job.title or ""
        desc = raw_job.description or ""
        text = f"{title} {desc}".lower()

        category = "Other"
        if "frontend" in text or "react" in text or "vue" in text or "ui" in text:
            category = "Frontend"
        elif "backend" in text or "node" in text or "python" in text or "java" in text or "api" in text:
            category = "Backend"
        elif "full stack" in text or "fullstack" in text:
            category = "Full Stack"
        elif "ai" in text or "machine learning" in text or "ml" in text or "deep learning" in text:
            category = "AI/ML"
        elif "mobile" in text or "android" in text or "ios" in text or "flutter" in text:
            category = "Mobile"
        elif "data" in text or "analytics" in text or "sql" in text:
            category = "Data"

        remote = "remote" in text or "work from home" in text
        skills = []
        common_skills = ["Python", "React", "JavaScript", "TypeScript", "Node.js", "Java", "C++", "SQL", "AWS", "Docker", "Git"]
        for skill in common_skills:
            if skill.lower() in text:
                skills.append(skill)

        return {
            "role": raw_job.title or "Internship Position",
            "skills": skills,
            "category": category,
            "remote": remote,
            "stipend": None
        }

    async def _process_single_job(self, db: Session, raw_job: RawJob, retries=3):
        if not self.model:
            structured_data = self._fallback_process(raw_job)
            self._save_internship_and_mark_processed(db, raw_job, structured_data)
            return

        prompt = prompt_template.format(
            title=raw_job.title or "Unknown",
            description=raw_job.description or ""
        )
        
        for attempt in range(retries):
            try:
                response = self.model.generate_content(prompt)
                structured_data = self._parse_gemini_response(response.text)
                self._save_internship_and_mark_processed(db, raw_job, structured_data)
                break
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON for raw_job {raw_job.id} on attempt {attempt+1}")
                if attempt == retries - 1:
                    db.rollback()
                    fallback_data = self._fallback_process(raw_job)
                    self._save_internship_and_mark_processed(db, raw_job, fallback_data)
            except Exception as e:
                logger.error(f"Error processing raw_job {raw_job.id} on attempt {attempt+1}: {e}")
                db.rollback()
                if attempt == retries - 1:
                    fallback_data = self._fallback_process(raw_job)
                    self._save_internship_and_mark_processed(db, raw_job, fallback_data)
            
            await asyncio.sleep(2)

    def _save_internship_and_mark_processed(self, db: Session, raw_job: RawJob, structured_data: dict):
        try:
            category = structured_data.get("category", "Other")
            valid_categories = ["Frontend", "Backend", "Full Stack", "AI/ML", "Mobile", "Data", "Other"]
            if category not in valid_categories:
                category = "Other"

            skills = structured_data.get("skills", [])
            if isinstance(skills, str):
                skills = [s.strip() for s in skills.split(",") if s.strip()]
            elif not isinstance(skills, list):
                skills = []
            skills = [str(s) for s in skills if s]

            existing_internship = db.query(Internship).filter(Internship.apply_link == raw_job.apply_link).first()
            if not existing_internship:
                new_internship = Internship(
                    role=structured_data.get("role") or raw_job.title or "Internship Position",
                    company=raw_job.company or "Unknown Company",
                    location=raw_job.location or "Not specified",
                    skills=skills,
                    category=category,
                    remote=bool(structured_data.get("remote", False)),
                    stipend=structured_data.get("stipend"),
                    apply_link=raw_job.apply_link,
                    source=raw_job.source
                )
                db.add(new_internship)

            raw_job.processed = True
            db.commit()
            logger.info(f"Successfully processed raw_job {raw_job.id}: {structured_data.get('role')}")
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to save processed internship for raw_job {raw_job.id}: {e}")
            try:
                raw_job.processed = True
                db.commit()
            except Exception as inner_e:
                db.rollback()
                logger.error(f"Failed to mark raw_job {raw_job.id} as processed: {inner_e}")
