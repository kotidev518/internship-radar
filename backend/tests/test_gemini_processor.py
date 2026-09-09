import pytest
from unittest.mock import MagicMock, AsyncMock
from services.gemini_processor import GeminiProcessor
from database.models import RawJob, Internship

def test_parse_gemini_response_clean():
    processor = GeminiProcessor()
    text = '{"role": "Frontend Intern", "skills": ["React"], "category": "Frontend", "remote": true, "stipend": "10k"}'
    data = processor._parse_gemini_response(text)
    assert data["role"] == "Frontend Intern"
    assert data["skills"] == ["React"]

def test_parse_gemini_response_markdown_block():
    processor = GeminiProcessor()
    text = '```json\n{"role": "Backend Intern", "skills": ["Python"], "category": "Backend", "remote": false, "stipend": null}\n```'
    data = processor._parse_gemini_response(text)
    assert data["role"] == "Backend Intern"
    assert data["category"] == "Backend"

def test_fallback_process():
    processor = GeminiProcessor()
    raw = RawJob(id=1, title="React Developer Intern", description="Work with React and TypeScript remote", company="Acme", apply_link="https://example.com/1")
    data = processor._fallback_process(raw)
    assert data["role"] == "React Developer Intern"
    assert data["category"] == "Frontend"
    assert data["remote"] is True
    assert "React" in data["skills"]

def test_save_internship_and_mark_processed(mocker):
    processor = GeminiProcessor()
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    raw_job = RawJob(id=1, title="AI Intern", company="AI Corp", location="Remote", apply_link="https://example.com/ai", source="LinkedIn", processed=False)
    structured_data = {
        "role": "AI Research Intern",
        "skills": "Python, PyTorch", # Test string skills handling
        "category": "AI/ML",
        "remote": True,
        "stipend": "$1000/mo"
    }

    processor._save_internship_and_mark_processed(mock_db, raw_job, structured_data)

    assert raw_job.processed is True
    assert mock_db.add.called
    assert mock_db.commit.called
