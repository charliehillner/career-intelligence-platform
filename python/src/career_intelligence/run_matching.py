from career_intelligence.db.repository import (
    get_job_requirements,
    get_person_skills,
)
from career_intelligence.matching.engine import (
    calculate_job_matches,
)


def main():
    person_skills = get_person_skills(
        "Synthetic Candidate"
    )

    jobs = get_job_requirements()

    results = calculate_job_matches(
        person_skills,
        jobs,
    )

    print()
    print("=== Career Intelligence V1 Job Ranking ===")
    print()

    for rank, result in enumerate(results, start=1):
        print(
            f"{rank:>2}. "
            f"{result.job_title:<35} "
            f"{result.qualification_fit:>6.1%}"
        )

        for skill in result.skill_results:
            print(
                f"      {skill.skill_name:<20} "
                f"Skill: {skill.skill_match:>6.1%}  "
                f"Prof: "
                f"{skill.proficiency_match if skill.proficiency_match is not None else '-'}  "
                f"Exp: "
                f"{skill.experience_match if skill.experience_match is not None else '-'}"
            )

        print()


if __name__ == "__main__":
    main()