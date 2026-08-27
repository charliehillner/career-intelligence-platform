def skill_match(
    proficiency_match_value: float | None = None,
    experience_match_value: float | None = None,
) -> float:
    """
    Aggregate the available V1 matching components for one skill.

    Available components contribute equally.

    At least one component must be available.
    """
    components = [
        value
        for value in (
            proficiency_match_value,
            experience_match_value,
        )
        if value is not None
    ]

    if not components:
        raise ValueError("at least one matching component must be provided")

    for value in components:
        if not 0.0 <= value <= 1.0:
            raise ValueError("matching components must lie between 0 and 1")

    return sum(components) / len(components)