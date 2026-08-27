import pytest

from career_intelligence.matching import qualification_fit


def test_qualification_fit():
    result = qualification_fit([1.0, 0.75, 0.5])

    assert result == pytest.approx(0.75)


def test_perfect_qualification_fit():
    assert qualification_fit([1.0, 1.0, 1.0]) == 1.0


def test_zero_qualification_fit():
    assert qualification_fit([0.0, 0.0]) == 0.0


def test_single_skill():
    assert qualification_fit([0.8]) == 0.8


def test_empty_skill_list_raises_error():
    with pytest.raises(ValueError):
        qualification_fit([])


def test_skill_match_above_one_raises_error():
    with pytest.raises(ValueError):
        qualification_fit([0.8, 1.1])


def test_skill_match_below_zero_raises_error():
    with pytest.raises(ValueError):
        qualification_fit([0.8, -0.1])