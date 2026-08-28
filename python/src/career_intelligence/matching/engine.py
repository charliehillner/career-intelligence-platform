from dataclasses import dataclass

from .experience import experience_match
from .proficiency import proficiency_match
from .qualification import qualification_fit
from .skill import skill_match


@dataclass
class SkillMatchResult:
    skill_name: str
    proficiency_match: float | None
    experience_match: float | None
    skill_match: float
    missing_skill: bool


@dataclass
class JobMatchResult:
    job_posting_key: int
    source_job_id: str
    job_title: str
    qualification_fit: float
    skill_results: list[SkillMatchResult]


def calculate_job_match(
    person_skills: dict[str, dict],
    job: dict,
) -> JobMatchResult:
    skill_results = []

    for requirement in job["requirements"]:
        skill_name = requirement["skill_name"]

        personal_skill = person_skills.get(skill_name)

        # V1 rule:
        # Required skill absent from personal profile -> skill match = 0.
        if personal_skill is None:
            skill_results.append(
                SkillMatchResult(
                    skill_name=skill_name,
                    proficiency_match=None,
                    experience_match=None,
                    skill_match=0.0,
                    missing_skill=True,
                )
            )
            continue

        proficiency_match_value = None
        experience_match_value = None

        required_proficiency = requirement[
            "required_proficiency_rank"
        ]
        personal_proficiency = personal_skill[
            "proficiency_rank"
        ]

        if (
            required_proficiency is not None
            and personal_proficiency is not None
        ):
            proficiency_match_value = proficiency_match(
                personal_rank=personal_proficiency,
                required_rank=required_proficiency,
            )

        required_experience = requirement[
            "required_years_experience"
        ]
        personal_experience = personal_skill[
            "years_experience"
        ]

        if (
            required_experience is not None
            and personal_experience is not None
        ):
            experience_match_value = experience_match(
                personal_years=personal_experience,
                required_years=required_experience,
            )

        match_value = skill_match(
            proficiency_match_value=proficiency_match_value,
            experience_match_value=experience_match_value,
        )

        skill_results.append(
            SkillMatchResult(
                skill_name=skill_name,
                proficiency_match=proficiency_match_value,
                experience_match=experience_match_value,
                skill_match=match_value,
                missing_skill=False,
            )
        )

    qualification = qualification_fit(
        [result.skill_match for result in skill_results]
    )

    return JobMatchResult(
        job_posting_key=job["job_posting_key"],
        source_job_id=job["source_job_id"],
        job_title=job["job_title"],
        qualification_fit=qualification,
        skill_results=skill_results,
    )

def calculate_job_matches(
    person_skills: dict[str, dict],
    jobs: list[dict],
) -> list[JobMatchResult]:
    results = [
        calculate_job_match(person_skills, job)
        for job in jobs
    ]

    return sorted(
        results,
        key=lambda result: result.qualification_fit,
        reverse=True,
    )