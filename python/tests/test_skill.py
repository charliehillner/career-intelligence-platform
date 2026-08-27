import pytest

from career_intelligence.matching import skill_match


def test_skill_match_with_both_components():
    assert skill_match(1.0, 0.5) == 0.75


def test_skill_match_with_only_proficiency():
    assert skill_match(proficiency_match_value=0.8) == 0.8


def test_skill_match_with_only_experience():
    assert skill_match(experience_match_value=0.6) == 0.6


def test_skill_match_without_components_raises_error():
    with pytest.raises(ValueError):
        skill_match()


def test_skill_match_rejects_values_above_one():
    with pytest.raises(ValueError):
        skill_match(1.1, 0.5)


def test_skill_match_rejects_values_below_zero():
    with pytest.raises(ValueError):
        skill_match(-0.1, 0.5)