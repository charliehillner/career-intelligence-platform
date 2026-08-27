def experience_match(
    personal_years: float,
    required_years: float,
) -> float:
    """
    Calculate the V1 experience match.

    For a positive experience requirement:

        match = min(1, personal_years / required_years)

    Exceeding the required experience is not penalized.
    """
    if personal_years < 0:
        raise ValueError("personal_years must not be negative")

    if required_years <= 0:
        raise ValueError("required_years must be greater than zero")

    return min(1.0, personal_years / required_years)