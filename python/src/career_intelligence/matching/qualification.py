def qualification_fit(skill_matches: list[float]) -> float:
    """
    Calculate the V1 Qualification Fit.

    In V1:

        Q(P, J) = m_Skills(P, J)

    All required skills contribute equally.
    """
    if not skill_matches:
        raise ValueError("at least one skill match must be provided")

    for value in skill_matches:
        if not 0.0 <= value <= 1.0:
            raise ValueError("skill matches must lie between 0 and 1")

    return sum(skill_matches) / len(skill_matches)