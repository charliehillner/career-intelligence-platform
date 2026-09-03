import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ExtractedSkillRequirement:
    skill_name: str
    required_proficiency: str | None = None
    required_years_experience: float | None = None


SKILL_PATTERNS: dict[str, tuple[str, ...]] = {
    "Python": (
        r"\bpython\b",
    ),
    "R": (
        r"\br programming\b",
        r"\br language\b",
        r"\br statistical programming\b",
        r"\br\b",
    ),
    "SQL": (
        r"\bsql\b",
    ),
    "Shiny": (
        r"\br shiny\b",
        r"\bshiny\b",
    ),
    "SAS": (
        r"\bsas\b",
    ),
    "Power BI": (
        r"\bpower\s*bi\b",
    ),
    "Docker": (
        r"\bdocker\b",
    ),
    "Java": (
        r"\bjava\b",
    ),
    "Machine Learning": (
        r"\bmachine learning\b",
    ),
    "Azure": (
        r"\bazure\b",
    ),
    "Kubernetes": (
        r"\bkubernetes\b",
    ),
    "Spark": (
        r"\bapache spark\b",
        r"\bspark\b",
    ),
    "Spring Boot": (
        r"\bspring boot\b",
    ),
    "Statistics": (
        r"\bstatistics\b",
        r"\bstatistical methods?\b",
        r"\bstatistical analysis\b",
    ),
}

def extract_skill_requirements(
    text: str,
) -> list[ExtractedSkillRequirement]:
    if not text or not text.strip():
        return []

    extracted: list[ExtractedSkillRequirement] = []

    for skill_name, patterns in SKILL_PATTERNS.items():
        if any(
            re.search(pattern, text, flags=re.IGNORECASE)
            for pattern in patterns
        ):
            extracted.append(
                ExtractedSkillRequirement(
                    skill_name=skill_name,
                )
            )

    return extracted