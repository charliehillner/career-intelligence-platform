import pytest

from career_intelligence.matching import experience_match


def test_exact_experience_match():
    assert experience_match(3.0, 3.0) == 1.0


def test_exceeding_required_experience_is_not_penalized():
    assert experience_match(5.0, 3.0) == 1.0


def test_partial_experience_match():
    assert experience_match(2.0, 4.0) == 0.5


def test_zero_personal_experience():
    assert experience_match(0.0, 4.0) == 0.0


def test_negative_personal_experience_raises_error():
    with pytest.raises(ValueError):
        experience_match(-1.0, 3.0)


def test_zero_required_experience_raises_error():
    with pytest.raises(ValueError):
        experience_match(2.0, 0.0)


def test_negative_required_experience_raises_error():
    with pytest.raises(ValueError):
        experience_match(2.0, -1.0)