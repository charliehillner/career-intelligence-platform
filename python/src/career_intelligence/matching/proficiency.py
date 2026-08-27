def proficiency_match(
    personal_rank: int,
    required_rank: int,
    min_rank: int = 1,
    max_rank: int = 4,
) -> float:
    """
    Calculate the V1 proficiency match.

    The model uses an asymmetric squared rank loss:

        loss = (max(0, required_rank - personal_rank)
                / (max_rank - min_rank)) ** 2

        match = 1 - loss

    Exceeding the required proficiency is not penalized.
    """
    if max_rank <= min_rank:
        raise ValueError("max_rank must be greater than min_rank")

    if not min_rank <= personal_rank <= max_rank:
        raise ValueError("personal_rank must lie within the proficiency scale")

    if not min_rank <= required_rank <= max_rank:
        raise ValueError("required_rank must lie within the proficiency scale")

    rank_deficit = max(0, required_rank - personal_rank)
    normalized_deficit = rank_deficit / (max_rank - min_rank)

    loss = normalized_deficit**2

    return 1.0 - loss