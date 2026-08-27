import pytest

from career_intelligence.matching import (
    experience_match,
    proficiency_match,
    qualification_fit,
    skill_match,
)


def test_complete_job_match():
    # ------------------------------------------------------------------
    # Synthetic person profile
    #
    # Python: Advanced, 3 years
    # SQL: Intermediate, 2 years
    # Statistics: Expert, 6 years
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Synthetic job requirements
    #
    # Python: Advanced, 3 years
    # SQL: Advanced, 4 years
    # Statistics: Advanced, 3 years
    # ------------------------------------------------------------------

    python_proficiency = proficiency_match(
        personal_rank=3,
        required_rank=3,
    )
    python_experience = experience_match(
        personal_years=3.0,
        required_years=3.0,
    )
    python_match = skill_match(
        python_proficiency,
        python_experience,
    )

    sql_proficiency = proficiency_match(
        personal_rank=2,
        required_rank=3,
    )
    sql_experience = experience_match(
        personal_years=2.0,
        required_years=4.0,
    )
    sql_match = skill_match(
        sql_proficiency,
        sql_experience,
    )

    statistics_proficiency = proficiency_match(
        personal_rank=4,
        required_rank=3,
    )
    statistics_experience = experience_match(
        personal_years=6.0,
        required_years=3.0,
    )
    statistics_match = skill_match(
        statistics_proficiency,
        statistics_experience,
    )

    result = qualification_fit(
        [
            python_match,
            sql_match,
            statistics_match,
        ]
    )

    expected_sql_match = ((8 / 9) + 0.5) / 2
    expected_result = (
        1.0
        + expected_sql_match
        + 1.0
    ) / 3

    assert result == pytest.approx(expected_result)


def test_complete_job_match_with_missing_skill():
    # Python:
    # Person: Advanced, 3 years
    # Job:    Advanced, 3 years
    python_proficiency = proficiency_match(3, 3)
    python_experience = experience_match(3.0, 3.0)

    python_match = skill_match(
        python_proficiency,
        python_experience,
    )

    # Statistics:
    # Person: Expert, 6 years
    # Job:    Advanced, 3 years
    statistics_proficiency = proficiency_match(4, 3)
    statistics_experience = experience_match(6.0, 3.0)

    statistics_match = skill_match(
        statistics_proficiency,
        statistics_experience,
    )

    # SAS:
    # Required by the job, but absent from the person's profile.
    # This is a skill gap, not missing information.
    sas_match = 0.0

    result = qualification_fit(
        [
            python_match,
            statistics_match,
            sas_match,
        ]
    )

    assert result == pytest.approx(2 / 3)