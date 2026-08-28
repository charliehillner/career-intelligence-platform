import os

import psycopg
from psycopg.rows import dict_row


def get_connection():
    return psycopg.connect(
        host=os.getenv("CI_DB_HOST", "localhost"),
        port=os.getenv("CI_DB_PORT", "5433"),
        dbname=os.getenv("CI_DB_NAME", "career_intelligence"),
        user=os.getenv("CI_DB_USER", "career_user"),
        password=os.getenv("CI_DB_PASSWORD", "career_password"),
        row_factory=dict_row,
    )


def get_person_skills(person_name: str) -> dict[str, dict]:
    query = """
        SELECT
            s.skill_name,
            prof.ordinal_rank AS proficiency_rank,
            fps.years_experience
        FROM fact_person_skill fps
        JOIN dim_person p
            ON p.person_key = fps.person_key
        JOIN dim_skill s
            ON s.skill_key = fps.skill_key
        LEFT JOIN dim_proficiency prof
            ON prof.proficiency_key = fps.proficiency_key
        WHERE p.person_name = %s
        ORDER BY s.skill_name;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (person_name,))
            rows = cur.fetchall()

    return {
        row["skill_name"]: {
            "proficiency_rank": row["proficiency_rank"],
            "years_experience": (
                float(row["years_experience"])
                if row["years_experience"] is not None
                else None
            ),
        }
        for row in rows
    }


def get_job_requirements() -> list[dict]:
    query = """
        SELECT
            j.job_posting_key,
            j.source_job_id,
            j.job_title,
            s.skill_name,
            prof.ordinal_rank AS required_proficiency_rank,
            b.required_years_experience
        FROM fact_job_posting j
        JOIN bridge_job_skill b
            ON b.job_posting_key = j.job_posting_key
        JOIN dim_skill s
            ON s.skill_key = b.skill_key
        LEFT JOIN dim_proficiency prof
            ON prof.proficiency_key = b.required_proficiency_key
        ORDER BY
            j.job_posting_key,
            s.skill_name;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    jobs: dict[int, dict] = {}

    for row in rows:
        job_key = row["job_posting_key"]

        if job_key not in jobs:
            jobs[job_key] = {
                "job_posting_key": job_key,
                "source_job_id": row["source_job_id"],
                "job_title": row["job_title"],
                "requirements": [],
            }

        jobs[job_key]["requirements"].append(
            {
                "skill_name": row["skill_name"],
                "required_proficiency_rank": row[
                    "required_proficiency_rank"
                ],
                "required_years_experience": (
                    float(row["required_years_experience"])
                    if row["required_years_experience"] is not None
                    else None
                ),
            }
        )

    return list(jobs.values())