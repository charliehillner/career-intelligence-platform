
from datetime import datetime

from career_intelligence.normalization.job_text import (
    build_observable_text,
)
from career_intelligence.normalization.location import normalize_adzuna_location
from career_intelligence.normalization.models import (
    NormalizedJob,
)
from career_intelligence.normalization.skill_extractor import (
    extract_skill_requirements,
)


def normalize_adzuna_job(job: dict) -> NormalizedJob:
    source_job_id = str(job["id"])
    title = job["title"].strip()

    company = (job.get("company") or {}).get("display_name")
    location = normalize_adzuna_location(job.get("location"))

    created = job.get("created")
    created_at = (
        datetime.fromisoformat(created.replace("Z", "+00:00"))
        if created
        else None
    )

    observable_text = build_observable_text(job)

    skills = tuple(
        extract_skill_requirements(observable_text)
    )

    return NormalizedJob(
        source="adzuna",
        source_job_id=source_job_id,
        title=title,
        company=company,
        location=location,
        created_at=created_at,
        skills=skills,
    )
