from dataclasses import dataclass
from datetime import datetime

from career_intelligence.normalization.skill_extractor import (
    ExtractedSkillRequirement,
)


@dataclass(frozen=True)
class NormalizedLocation:
    country: str
    region: str | None = None
    city: str | None = None


@dataclass(frozen=True)
class NormalizedJob:
    source: str
    source_job_id: str
    title: str
    company: str | None
    location: NormalizedLocation | None
    created_at: datetime | None
    skills: tuple[ExtractedSkillRequirement, ...]
