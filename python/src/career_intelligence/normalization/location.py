
from career_intelligence.normalization.models import (
    NormalizedLocation,
)


def normalize_adzuna_location(
    location: dict | None,
) -> NormalizedLocation | None:
    if not location:
        return None

    area = location.get("area")

    if not isinstance(area, list) or not area:
        return None

    parts = [
        part.strip()
        for part in area
        if isinstance(part, str) and part.strip()
    ]

    if not parts:
        return None

    country = parts[0]
    region = parts[1] if len(parts) >= 2 else None
    city = parts[2] if len(parts) == 3 else None

    return NormalizedLocation(
        country=country,
        region=region,
        city=city,
    )
