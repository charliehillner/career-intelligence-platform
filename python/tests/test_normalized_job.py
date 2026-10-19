from datetime import datetime, timezone

from career_intelligence.normalization import (
    ExtractedSkillRequirement,
    NormalizedJob,
)
from career_intelligence.normalization.models import NormalizedLocation


def test_normalized_job_creation():
    job = NormalizedJob(
        source="adzuna",
        source_job_id="5688461276",
        title="Python Developer / Data Scientist",
        company="eClear AG",
        location=NormalizedLocation(
            country="Deutschland",
            region="Berlin",
            city="Berlin",
        ),
        created_at=datetime(
            2026, 4, 3, 10, 20, 41,
            tzinfo=timezone.utc,
        ),
        skills=(
            ExtractedSkillRequirement(
                skill_name="Python",
            ),
        ),
    )

    assert job.source == "adzuna"
    assert job.source_job_id == "5688461276"
    assert job.company == "eClear AG"
    assert len(job.skills) == 1
    assert job.skills[0].skill_name == "Python"
    assert job.skills[0].required_proficiency is None
    assert job.skills[0].required_years_experience is None
