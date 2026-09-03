from collections import Counter

from career_intelligence.normalization import (
    build_observable_text,
    extract_skill_requirements,
)
from career_intelligence.sources.adzuna import search_jobs

def value_or_missing(value):
    if value is None:
        return "<missing>"

    if isinstance(value, str) and not value.strip():
        return "<empty>"

    return value


def main():
    data = search_jobs(
        query="Python Data Scientist",
        country="de",
        results_per_page=10,
    )

    jobs = data["results"]

    print(f"Returned jobs: {len(jobs)}")
    print(f"Total matching jobs: {data['count']}")
    print()

    key_counts = Counter()

    for job in jobs:
        key_counts.update(job.keys())

    print("=== Top-Level Field Availability ===")
    print()

    for key, count in sorted(key_counts.items()):
        print(
            f"{key:<25} "
            f"{count:>2}/{len(jobs)} "
            f"({count / len(jobs):>6.1%})"
        )

    print("\n=== Core Field Values ===\n")

    for i, job in enumerate(jobs, start=1):
        company = job.get("company") or {}
        location = job.get("location") or {}
        category = job.get("category") or {}

        print(f"Job {i}")
        print(f"  ID:       {value_or_missing(job.get('id'))}")
        print(f"  Title:    {value_or_missing(job.get('title'))}")
        print(
            f"  Company:  "
            f"{value_or_missing(company.get('display_name'))}"
        )
        print(
            f"  Location: "
            f"{value_or_missing(location.get('display_name'))}"
        )
        print(
            f"  Area:     "
            f"{value_or_missing(location.get('area'))}"
        )
        print(
            f"  Category: "
            f"{value_or_missing(category.get('label'))}"
        )
        print(
            f"  Created:  "
            f"{value_or_missing(job.get('created'))}"
        )
        print(
            f"  Description length: "
            f"{len(job.get('description', ''))}"
        )
        print()

        text = build_observable_text(job)
        
        skills = extract_skill_requirements(text)

        skill_names = [
            skill.skill_name
            for skill in skills
        ]
        print(
            f"  Skills:   "
            f"{', '.join(skill_names) if skill_names else '<none>'}"
        )
        print()


if __name__ == "__main__":
    main()