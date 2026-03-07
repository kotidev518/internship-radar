"""Seed the database with sample internship and application records."""
import os
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Internship, Application
from datetime import datetime, timedelta

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

# Ensure tables exist
Base.metadata.create_all(bind=engine)

# --- Sample Internships ---
internships_data = [
    {
        "role": "Frontend Developer Intern",
        "company": "Google",
        "location": "Bangalore, India",
        "skills": ["React", "TypeScript", "CSS", "Next.js"],
        "category": "Web Development",
        "remote": False,
        "stipend": "₹80,000/month",
        "apply_link": "https://careers.google.com/intern-frontend-2026",
        "source": "Google Careers",
    },
    {
        "role": "Machine Learning Intern",
        "company": "Microsoft",
        "location": "Hyderabad, India",
        "skills": ["Python", "TensorFlow", "PyTorch", "NumPy"],
        "category": "AI/ML",
        "remote": False,
        "stipend": "₹75,000/month",
        "apply_link": "https://careers.microsoft.com/ml-intern-2026",
        "source": "Microsoft Careers",
    },
    {
        "role": "Backend Engineer Intern",
        "company": "Amazon",
        "location": "Remote",
        "skills": ["Java", "AWS", "Spring Boot", "Microservices"],
        "category": "Backend Development",
        "remote": True,
        "stipend": "₹70,000/month",
        "apply_link": "https://amazon.jobs/backend-intern-2026",
        "source": "Amazon Jobs",
    },
    {
        "role": "Data Science Intern",
        "company": "Flipkart",
        "location": "Bangalore, India",
        "skills": ["Python", "SQL", "Pandas", "Scikit-learn"],
        "category": "Data Science",
        "remote": False,
        "stipend": "₹60,000/month",
        "apply_link": "https://flipkart.com/careers/ds-intern-2026",
        "source": "Flipkart Careers",
    },
    {
        "role": "Full Stack Developer Intern",
        "company": "Razorpay",
        "location": "Bangalore, India",
        "skills": ["React", "Node.js", "PostgreSQL", "Docker"],
        "category": "Web Development",
        "remote": False,
        "stipend": "₹50,000/month",
        "apply_link": "https://razorpay.com/careers/fullstack-intern-2026",
        "source": "Razorpay Careers",
    },
    {
        "role": "Cloud Engineering Intern",
        "company": "IBM",
        "location": "Remote",
        "skills": ["AWS", "Azure", "Terraform", "Kubernetes"],
        "category": "Cloud/DevOps",
        "remote": True,
        "stipend": "₹55,000/month",
        "apply_link": "https://ibm.com/careers/cloud-intern-2026",
        "source": "IBM Careers",
    },
    {
        "role": "Mobile App Developer Intern",
        "company": "PhonePe",
        "location": "Pune, India",
        "skills": ["Flutter", "Dart", "Firebase", "REST APIs"],
        "category": "Mobile Development",
        "remote": False,
        "stipend": "₹45,000/month",
        "apply_link": "https://phonepe.com/careers/mobile-intern-2026",
        "source": "PhonePe Careers",
    },
    {
        "role": "Cybersecurity Intern",
        "company": "Palo Alto Networks",
        "location": "Remote",
        "skills": ["Network Security", "Python", "SIEM", "Penetration Testing"],
        "category": "Cybersecurity",
        "remote": True,
        "stipend": "₹65,000/month",
        "apply_link": "https://paloaltonetworks.com/intern-cyber-2026",
        "source": "Palo Alto Careers",
    },
    {
        "role": "UI/UX Design Intern",
        "company": "Swiggy",
        "location": "Bangalore, India",
        "skills": ["Figma", "Adobe XD", "User Research", "Prototyping"],
        "category": "Design",
        "remote": False,
        "stipend": "₹40,000/month",
        "apply_link": "https://swiggy.com/careers/design-intern-2026",
        "source": "Swiggy Careers",
    },
    {
        "role": "DevOps Intern",
        "company": "Atlassian",
        "location": "Remote",
        "skills": ["Docker", "Jenkins", "CI/CD", "Linux", "Bash"],
        "category": "Cloud/DevOps",
        "remote": True,
        "stipend": "₹70,000/month",
        "apply_link": "https://atlassian.com/careers/devops-intern-2026",
        "source": "Atlassian Careers",
    },
    {
        "role": "NLP Research Intern",
        "company": "OpenAI",
        "location": "Remote",
        "skills": ["Python", "Transformers", "NLP", "HuggingFace"],
        "category": "AI/ML",
        "remote": True,
        "stipend": "$8,000/month",
        "apply_link": "https://openai.com/careers/nlp-intern-2026",
        "source": "OpenAI Careers",
    },
    {
        "role": "Blockchain Developer Intern",
        "company": "Polygon",
        "location": "Remote",
        "skills": ["Solidity", "Ethereum", "Web3.js", "Smart Contracts"],
        "category": "Blockchain",
        "remote": True,
        "stipend": "₹60,000/month",
        "apply_link": "https://polygon.technology/careers/blockchain-intern-2026",
        "source": "Polygon Careers",
    },
]

print("Inserting sample internships...")
created_internships = []
for data in internships_data:
    # Check if already exists
    existing = session.query(Internship).filter(Internship.apply_link == data["apply_link"]).first()
    if existing:
        print(f"  Skipped (exists): {data['role']} at {data['company']}")
        created_internships.append(existing)
        continue
    intern = Internship(**data)
    session.add(intern)
    session.flush()  # Get the ID
    created_internships.append(intern)
    print(f"  Added: {data['role']} at {data['company']}")

session.commit()

# --- Sample Applications (track a few internships) ---
applications_data = [
    {"internship_idx": 0, "status": "applied", "notes": "Applied via referral from a friend at Google.", "applied_date": datetime.utcnow() - timedelta(days=5)},
    {"internship_idx": 1, "status": "interview", "notes": "Completed first round, waiting for ML system design round.", "applied_date": datetime.utcnow() - timedelta(days=10)},
    {"internship_idx": 2, "status": "saved", "notes": "Looks interesting, need to prep for Java interviews first."},
    {"internship_idx": 4, "status": "applied", "notes": "Submitted application with portfolio link.", "applied_date": datetime.utcnow() - timedelta(days=3)},
    {"internship_idx": 10, "status": "offer", "notes": "Received offer! Need to decide by end of month.", "applied_date": datetime.utcnow() - timedelta(days=20)},
]

print("\nInserting sample applications...")
for app_data in applications_data:
    internship = created_internships[app_data["internship_idx"]]
    # Check if application already exists for this internship
    existing = session.query(Application).filter(Application.internship_id == internship.id).first()
    if existing:
        print(f"  Skipped (exists): Application for {internship.role} at {internship.company}")
        continue
    app = Application(
        internship_id=internship.id,
        status=app_data["status"],
        notes=app_data.get("notes"),
        applied_date=app_data.get("applied_date"),
    )
    session.add(app)
    print(f"  Added: [{app_data['status'].upper()}] {internship.role} at {internship.company}")

session.commit()
session.close()

print(f"\n✅ Done! Inserted {len(internships_data)} internships and {len(applications_data)} applications.")
