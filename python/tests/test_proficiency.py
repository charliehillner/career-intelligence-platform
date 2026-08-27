import pytest

from career_intelligence.matching import proficiency_match


def test_exact_proficiency_match():
    assert proficiency_match(3, 3) == 1.0


def test_exceeding_required_proficiency_is_not_penalized():
    assert proficiency_match(4, 3) == 1.0


def test_one_rank_deficit():
    result = proficiency_match(2, 3)

    assert result == pytest.approx(8 / 9)


def test_maximum_rank_deficit():
    assert proficiency_match(1, 4) == 0.0


def test_personal_rank_outside_scale_raises_error():
    with pytest.raises(ValueError):
        proficiency_match(0, 3)


def test_required_rank_outside_scale_raises_error():
    with pytest.raises(ValueError):
        proficiency_match(3, 5)


def test_invalid_scale_raises_error():
    with pytest.raises(ValueError):
        proficiency_match(2, 3, min_rank=4, max_rank=4)