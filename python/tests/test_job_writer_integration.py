
from datetime import datetime, timezone
from uuid import uuid4

from career_intelligence.db.writer import save_normalized_job
from career_intelligence.db.repository import get_connection
from career_intelligence.normalization.models import (
    NormalizedJob,
    NormalizedLocation,
)
from career_intelligence.normalization.skill_extractor import (
    ExtractedSkillRequirement,
)
import pytest



def test_save_normalized_job_is_repeatable(test_source_id):
    job = make_test_job(test_source_id)

    first_key = save_normalized_job(job)
    second_key = save_normalized_job(job)

    assert first_key == second_key

    saved_job = get_saved_job(test_source_id)

    assert saved_job["job_posting_key"] == first_key

    assert get_saved_skills(first_key) == {
        "Python",
        "SQL",
    }

def test_update_existing_job(test_source_id):
    original = make_test_job(
        source_job_id=test_source_id,
        title="Python Data Analyst",
        skill_names=("Python", "SQL"),
    )

    original_key = save_normalized_job(original)

    updated = make_test_job(
        source_job_id=test_source_id,
        title="Senior Python Developer",
        skill_names=("Python", "Docker"),
    )

    updated_key = save_normalized_job(updated)

    assert original_key == updated_key

    saved_job = get_saved_job(test_source_id)

    assert saved_job["job_title"] == "Senior Python Developer"

    assert get_saved_skills(updated_key) == {
        "Python",
        "Docker",
    }


def test_rollback_on_unknown_skill(test_source_id):
    original = make_test_job(
        source_job_id=test_source_id,
        title="Original Job",
        skill_names=("Python",),
    )

    job_key = save_normalized_job(original)

    invalid_update = make_test_job(
        source_job_id=test_source_id,
        title="Updated Job",
        skill_names=(
            "SQL",
            "DefinitelyNotACanonicalSkill_999",
        ),
    )

    with pytest.raises(
        ValueError,
        match="Unknown canonical skill",
    ):
        save_normalized_job(invalid_update)

    saved_job = get_saved_job(test_source_id)

    assert saved_job["job_posting_key"] == job_key
    assert saved_job["job_title"] == "Original Job"

    assert get_saved_skills(job_key) == {"Python"}


def test_save_job_without_skills(test_source_id):
    job = make_test_job(
        source_job_id=test_source_id,
        skill_names=(),
    )

    job_key = save_normalized_job(job)

    assert get_saved_job(test_source_id) is not None
    assert get_saved_skills(job_key) == set()


def test_reject_missing_publication_date(test_source_id):
    job = make_test_job(
        source_job_id=test_source_id,
        created_at=None,
    )

    with pytest.raises(
        ValueError,
        match="Publication date is required",
    ):
        save_normalized_job(job)

    assert get_saved_job(test_source_id) is None


@pytest.fixture
def test_source_id():
    source_job_id = str(uuid4())

    yield source_job_id

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM fact_job_posting
                WHERE source_name = %s
                  AND source_job_id = %s
                """,
                ("integration_test", source_job_id),
            )


def make_test_job(
    source_job_id: str,
    title: str = "Python Data Analyst",
    skill_names: tuple[str, ...] = ("Python", "SQL"),
    created_at: datetime | None = datetime(
        2026, 10, 19, tzinfo=timezone.utc
    ),
) -> NormalizedJob:
    return NormalizedJob(
        source="integration_test",
        source_job_id=source_job_id,
        title=title,
        company="Test Company",
        location=NormalizedLocation(
            country="Deutschland",
            region="Niedersachsen",
            city="Oldenburg",
        ),
        created_at=created_at,
        skills=tuple(
            ExtractedSkillRequirement(skill_name=name)
            for name in skill_names
        ),
    )


def get_saved_job(source_job_id: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT job_posting_key, job_title
                FROM fact_job_posting
                WHERE source_name = %s
                  AND source_job_id = %s
                """,
                ("integration_test", source_job_id),
            )
            return cur.fetchone()


def get_saved_skills(job_posting_key: int) -> set[str]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT s.skill_name
                FROM bridge_job_skill b
                JOIN dim_skill s
                    ON s.skill_key = b.skill_key
                WHERE b.job_posting_key = %s
                """,
                (job_posting_key,),
            )
            return {
                row["skill_name"]
                for row in cur.fetchall()
            }
