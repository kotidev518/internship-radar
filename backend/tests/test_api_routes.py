import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from database.connection import get_db
from datetime import datetime, timezone
from database.models import Internship, Application

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_get_internships_api(mocker):
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db

    mock_internship = Internship(
        id=1,
        role="Frontend Developer Intern",
        company="Tech Corp",
        location="Remote",
        skills=["React", "TypeScript"],
        category="Frontend",
        remote=True,
        stipend="$1000",
        apply_link="https://example.com/apply1",
        source="LinkedIn",
        created_at=datetime.now(timezone.utc)
    )
    mock_db.query.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [mock_internship]

    response = client.get("/api/internships")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["role"] == "Frontend Developer Intern"

    app.dependency_overrides.clear()

def test_search_internships_api(mocker):
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db

    mock_db.query.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = []

    response = client.get("/api/internships/search?q=React")
    assert response.status_code == 200
    assert response.json() == []

    app.dependency_overrides.clear()

def test_applications_api_create_and_update(mocker):
    mock_db = MagicMock()
    app.dependency_overrides[get_db] = lambda: mock_db

    now = datetime.now(timezone.utc)
    mock_internship = Internship(
        id=1,
        role="Dev",
        company="A",
        location="B",
        skills=[],
        category="Other",
        remote=False,
        apply_link="http://a.com",
        source="X",
        created_at=now
    )

    mock_db.query.return_value.filter.return_value.first.side_effect = [mock_internship, None]

    def set_app_id(obj):
        if isinstance(obj, Application):
            obj.id = 10
            obj.updated_at = now
            obj.internship = mock_internship

    mock_db.add.side_effect = set_app_id

    response = client.post("/api/applications", json={"internship_id": 1, "status": "saved"})
    assert response.status_code == 201

    app.dependency_overrides.clear()
