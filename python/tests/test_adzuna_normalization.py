
from datetime import datetime, timezone

from career_intelligence.normalization import (
    normalize_adzuna_job,
)
from career_intelligence.normalization.models import NormalizedLocation


def test_normalize_adzuna_job():
    raw_job = {
        "id": "12345",
        "title": "Python Developer",
        "company": {
            "display_name": "Example Company",
        },
        "location": {
            "area": ["Deutschland", "Berlin", "Berlin"],
            "display_name": "Berlin",
},
        "created": "2026-09-03T09:28:10Z",
        "description": "Experience with Python and SQL.",
    }

    job = normalize_adzuna_job(raw_job)

    assert job.source == "adzuna"
    assert job.source_job_id == "12345"
    assert job.title == "Python Developer"
    assert job.company == "Example Company"
    assert job.location == NormalizedLocation(
        country="Deutschland",
        region="Berlin",
        city="Berlin",
    )
    assert job.created_at == datetime(
        2026, 9, 3, 9, 28, 10,
        tzinfo=timezone.utc,
    )

    assert {
        skill.skill_name
        for skill in job.skills
    } == {"Python", "SQL"}


def test_normalize_adzuna_job_with_missing_optional_fields():
    raw_job = {
        "id": "67890",
        "title": "Data Analyst",
        "description": "",
    }

    job = normalize_adzuna_job(raw_job)

    assert job.company is None
    assert job.location is None
    assert job.created_at is None
    assert job.skills == ()
