# Gemini Processing Pipeline

## Overview

This document defines the AI preprocessing system used in the Internship Radar platform.

The AI preprocessing pipeline converts **raw scraped job descriptions** into **structured internship records** using the Gemini API.

The system performs the following tasks:

• normalize internship titles
• extract required technical skills
• classify internship category
• detect remote internships
• extract stipend information if available

Processed records are then inserted into the **internships database table**.

---

# Processing Pipeline

The AI processing pipeline runs after the scraper finishes collecting raw job data.

Pipeline flow:

Raw Job Data
↓
Gemini AI Processing
↓
JSON Validation
↓
Clean Internship Record
↓
Neon PostgreSQL

---

# AI Model

Recommended model:

Gemini 1.5 Flash

Reasons for choosing this model:

• fast inference speed
• very low cost
• strong structured extraction capability
• large context window

---

# Input Data

Each preprocessing task receives a record from the **raw_jobs table**.

Example raw record:

```json
{
 "title": "ReactJS Internship",
 "company": "StartupX",
 "location": "Remote",
 "description": "Looking for a React developer with knowledge of JavaScript, REST APIs and Git.",
 "apply_link": "https://example.com/apply"
}
```

---

# Prompt Design

The AI prompt must instruct the model to produce **strict JSON output**.

### Prompt Template

```text
Extract structured internship information from the following job description.

Return JSON with the fields:

role
skills
category
remote
stipend

Rules:

- Normalize the job title
- Extract only technical skills
- Category must be one of:
  Frontend
  Backend
  Full Stack
  AI/ML
  Mobile
  Data
  Other

- Remote must be true or false
- If stipend is not mentioned return null
- Return only valid JSON

Job Title:
{job_title}

Job Description:
{job_description}
```

---

# Example AI Response

```json
{
 "role": "React Developer Intern",
 "skills": ["React", "JavaScript", "REST API", "Git"],
 "category": "Frontend",
 "remote": true,
 "stipend": null
}
```

---

# JSON Output Schema

The AI output must match the following schema.

```json
{
 "role": "string",
 "skills": ["string"],
 "category": "string",
 "remote": "boolean",
 "stipend": "string | null"
}
```

Field definitions:

| Field    | Description                       |
| -------- | --------------------------------- |
| role     | normalized internship title       |
| skills   | list of detected technical skills |
| category | internship type                   |
| remote   | whether internship is remote      |
| stipend  | stipend information if present    |

---

# Validation Rules

Before inserting AI output into the database, validation checks must be performed.

Validation steps:

1. Ensure JSON parsing succeeds.
2. Ensure required fields exist.
3. Ensure skills is an array.
4. Ensure remote is boolean.
5. Ensure category belongs to allowed categories.

Example Python validation:

```python
allowed_categories = [
 "Frontend",
 "Backend",
 "Full Stack",
 "AI/ML",
 "Mobile",
 "Data",
 "Other"
]
```

If validation fails, the record should be retried or flagged.

---

# Error Handling

AI processing may fail due to malformed responses or API errors.

The system must handle these cases.

### Common failure scenarios

Invalid JSON response
API timeout
Rate limit exceeded
Missing fields

### Retry Strategy

If processing fails:

Retry up to 3 times.

Example logic:

```python
MAX_RETRIES = 3
```

If the record still fails after retries, mark it as failed for manual review.

---

# Batch Processing Strategy

Processing records individually is inefficient.

The system processes raw jobs in batches.

Example batch size:

20 records per batch

Batch workflow:

1. Fetch 20 unprocessed raw jobs
2. Send each record to Gemini
3. Validate responses
4. Insert clean records
5. Mark raw records as processed

Example query:

```sql
SELECT * FROM raw_jobs
WHERE processed = false
LIMIT 20;
```

---

# Deduplication Handling

Before inserting AI-processed records, check for duplicates.

Duplicate rule:

apply_link must be unique.

Example insertion rule:

```sql
INSERT INTO internships (...)
ON CONFLICT (apply_link) DO NOTHING;
```

This prevents duplicate internships across different sources.

---

# Cost Optimization

To reduce AI token usage:

• send only relevant job description sections
• limit prompt size
• remove unnecessary HTML

Recommended description length:

500–1000 tokens

---

# Logging

The system should log all preprocessing operations.

Logged data:

raw_job_id
processing_status
error_messages
timestamp

Example log entry:

```json
{
 "raw_job_id": 1021,
 "status": "success",
 "timestamp": "2026-03-07T09:10:00"
}
```

---

# Performance Expectations

Typical throughput:

20–40 records per minute

Daily processing volume:

300–500 internships

Monthly AI usage:

~6000 requests

---

# Reliability Improvements

Recommended improvements:

• batch processing
• structured prompt design
• strict JSON validation
• retry mechanisms
• detailed logging

These practices ensure reliable AI preprocessing.

---

# Summary

The Gemini preprocessing system transforms raw job listings into structured internship records using AI.

Key components:

• structured prompts
• JSON schema validation
• batch processing
• retry mechanisms
• duplicate prevention

This system enables the platform to reliably process **hundreds of internships daily** and maintain a high-quality internship database.
