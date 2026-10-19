
from datetime import datetime, timezone

from career_intelligence.db.writer import save_normalized_job
from career_intelligence.db.repository import get_connection
from career_intelligence.normalization.models import (
    NormalizedJob,
    NormalizedLocation,
)
from career_intelligence.normalization.skill_extractor import (
    ExtractedSkillRequirement,
)


def test_save_normalized_job_is_repeatable():
    job = NormalizedJob(
        source="integration_test",
        source_job_id="job-001",
        title="Python Data Analyst",
        company="Test Company",
        location=NormalizedLocation(
            country="Deutschland",
            region="Niedersachsen",
            city="Oldenburg",
        ),
        created_at=datetime(
            2026, 10, 19, tzinfo=timezone.utc
        ),
        skills=(
            ExtractedSkillRequirement("Python"),
            ExtractedSkillRequirement("SQL"),
        ),
    )

    try:
        first_key = save_normalized_job(job)
        second_key = save_normalized_job(job)

        assert first_key == second_key

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT COUNT(*) AS count
                    FROM fact_job_posting
                    WHERE source_name = %s
                      AND source_job_id = %s
                    """,
                    ("integration_test", "job-001"),
                )

                assert cur.fetchone()["count"] == 1

                cur.execute(
                    """
                    SELECT s.skill_name
                    FROM bridge_job_skill b
                    JOIN dim_skill s
                      ON s.skill_key = b.skill_key
                    WHERE b.job_posting_key = %s
                    """,
                    (first_key,),
                )

                skill_names = {
                    row["skill_name"]
                    for row in cur.fetchall()
                }

                assert skill_names == {"Python", "SQL"}

    finally:
        # Remove test posting without touching other jobs.
        # Associated skill rows are deleted via ON DELETE CASCADE.
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM fact_job_posting
                    WHERE source_name = %s
                      AND source_job_id = %s
                    """,
                    ("integration_test", "job-001"),
                )
