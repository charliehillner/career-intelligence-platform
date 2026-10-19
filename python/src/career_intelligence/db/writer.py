
from calendar import month_name
from datetime import timezone

from career_intelligence.db.repository import get_connection
from career_intelligence.normalization.models import NormalizedJob


def _upsert_date(cur, value):
    date_key = int(value.strftime("%Y%m%d"))

    cur.execute(
        """
        INSERT INTO dim_date (
            date_key, full_date, year, quarter,
            month, month_name
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (date_key) DO NOTHING
        """,
        (
            date_key,
            value,
            value.year,
            (value.month - 1) // 3 + 1,
            value.month,
            month_name[value.month],
        ),
    )

    return date_key


def _upsert_company(cur, company):
    if company is None:
        return None

    cur.execute(
        """
        INSERT INTO dim_company (company_name)
        VALUES (%s)
        ON CONFLICT (company_name)
        DO UPDATE SET company_name = EXCLUDED.company_name
        RETURNING company_key
        """,
        (company,),
    )

    return cur.fetchone()["company_key"]


def _upsert_location(cur, location):
    if location is None:
        return None

    cur.execute(
        """
        INSERT INTO dim_location (country, region, city)
        VALUES (%s, %s, %s)
        ON CONFLICT (country, region, city)
        DO UPDATE SET country = EXCLUDED.country
        RETURNING location_key
        """,
        (
            location.country,
            location.region,
            location.city,
        ),
    )

    return cur.fetchone()["location_key"]


def _resolve_skill_key(cur, skill_name):
    cur.execute(
        """
        SELECT skill_key
        FROM dim_skill
        WHERE skill_name = %s
        """,
        (skill_name,),
    )

    row = cur.fetchone()

    if row is None:
        raise ValueError(
            f"Unknown canonical skill: {skill_name}"
        )

    return row["skill_key"]


def _resolve_proficiency_key(cur, proficiency_name):
    if proficiency_name is None:
        return None

    cur.execute(
        """
        SELECT proficiency_key
        FROM dim_proficiency
        WHERE proficiency_name = %s
        """,
        (proficiency_name,),
    )

    row = cur.fetchone()

    if row is None:
        raise ValueError(
            f"Unknown proficiency: {proficiency_name}"
        )

    return row["proficiency_key"]


def save_normalized_job(job: NormalizedJob) -> int:
    """
    Insert or update one normalized job posting.

    Returns the internal job_posting_key.

    All writes occur in a single transaction.
    """

    if not job.source.strip():
        raise ValueError("Job source must not be empty")

    if not job.source_job_id.strip():
        raise ValueError("Source job ID must not be empty")

    if not job.title.strip():
        raise ValueError("Job title must not be empty")

    if job.created_at is None:
        raise ValueError("Publication date is required")

    # Date policy for MVP 1C: UTC calendar date.
    if (
        job.created_at.tzinfo is None
        or job.created_at.utcoffset() is None
    ):
        raise ValueError("Publication datetime must have a timezone")

    publication_date = (
        job.created_at.astimezone(timezone.utc).date()
    )

    with get_connection() as conn:
        with conn.cursor() as cur:
            date_key = _upsert_date(cur, publication_date)
            company_key = _upsert_company(cur, job.company)
            location_key = _upsert_location(cur, job.location)

            cur.execute(
                """
                INSERT INTO fact_job_posting (
                    source_name,
                    source_job_id,
                    job_title,
                    date_key,
                    company_key,
                    location_key,
                    job_profile_key
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, NULL
                )
                ON CONFLICT (source_name, source_job_id)
                WHERE source_name IS NOT NULL
                  AND source_job_id IS NOT NULL
                DO UPDATE SET
                    job_title = EXCLUDED.job_title,
                    date_key = EXCLUDED.date_key,
                    company_key = EXCLUDED.company_key,
                    location_key = EXCLUDED.location_key
                RETURNING job_posting_key
                """,
                (
                    job.source,
                    job.source_job_id,
                    job.title,
                    date_key,
                    company_key,
                    location_key,
                ),
            )

            job_posting_key = cur.fetchone()[
                "job_posting_key"
            ]

            # Full replacement of observed requirements.
            # An empty collection means no skills were observed.
            cur.execute(
                """
                DELETE FROM bridge_job_skill
                WHERE job_posting_key = %s
                """,
                (job_posting_key,),
            )

            for skill in job.skills:
                skill_key = _resolve_skill_key(
                    cur, skill.skill_name
                )

                proficiency_key = _resolve_proficiency_key(
                    cur, skill.required_proficiency
                )

                cur.execute(
                    """
                    INSERT INTO bridge_job_skill (
                        job_posting_key,
                        skill_key,
                        required_proficiency_key,
                        required_years_experience
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        job_posting_key,
                        skill_key,
                        proficiency_key,
                        skill.required_years_experience,
                    ),
                )

    return job_posting_key
