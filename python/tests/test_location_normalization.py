
from career_intelligence.normalization import (
    NormalizedLocation,
    normalize_adzuna_location,
)


def test_three_level_location():
    raw = {
        "area": ["Deutschland", "Niedersachsen", "Oldenburg"]
    }

    result = normalize_adzuna_location(raw)

    assert result == NormalizedLocation(
        country="Deutschland",
        region="Niedersachsen",
        city="Oldenburg",
    )


def test_country_only():
    result = normalize_adzuna_location({
        "area": ["Deutschland"]
    })

    assert result == NormalizedLocation(
        country="Deutschland",
        region=None,
        city=None,
    )


def test_deep_hierarchy():
    result = normalize_adzuna_location({
        "area": [
            "Deutschland",
            "Niedersachsen",
            "Oldenburg",
            "Innenstadt",
        ]
    })

    assert result == NormalizedLocation(
        country="Deutschland",
        region="Niedersachsen",
        city=None,
    )


def test_missing_location():
    assert normalize_adzuna_location(None) is None
    assert normalize_adzuna_location({}) is None
    assert normalize_adzuna_location({"area": []}) is None
