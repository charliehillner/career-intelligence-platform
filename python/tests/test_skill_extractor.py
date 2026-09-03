from career_intelligence.normalization.skill_extractor import (
    extract_skill_requirements,
)


def extracted_names(text: str) -> set[str]:
    return {
        requirement.skill_name
        for requirement in extract_skill_requirements(text)
    }


def test_extracts_explicit_skills():
    text = """
    Experience with R, Python and SAS is required.
    """

    assert extracted_names(text) == {
        "R",
        "Python",
        "SAS",
    }


def test_matching_is_case_insensitive():
    text = """
    Experience with PYTHON, sql and Power BI.
    """

    assert extracted_names(text) == {
        "Python",
        "SQL",
        "Power BI",
    }


def test_r_does_not_match_inside_words():
    text = """
    Clinical research experience and regulatory
    knowledge are required.
    """

    assert "R" not in extracted_names(text)


def test_sql_does_not_match_inside_words():
    text = """
    The candidate should have inquisqlitive thinking.
    """

    assert "SQL" not in extracted_names(text)


def test_extracts_r_shiny():
    text = """
    Applications will be developed using R/Shiny.
    """

    assert extracted_names(text) == {
        "R",
        "Shiny",
    }


def test_extracts_powerbi_without_space():
    text = """
    Experience creating PowerBI dashboards is desirable.
    """

    assert extracted_names(text) == {
        "Power BI",
    }


def test_returns_each_skill_only_once():
    text = """
    Python programming experience is required.
    The candidate will develop applications in Python.
    """

    skills = extract_skill_requirements(text)

    assert len(skills) == 1
    assert skills[0].skill_name == "Python"


def test_returns_empty_list_for_empty_text():
    assert extract_skill_requirements("") == []
    assert extract_skill_requirements("   ") == []


def test_requirement_details_are_unknown_in_presence_only_v1():
    text = """
    Experience with Python is required.
    """

    requirements = extract_skill_requirements(text)

    assert len(requirements) == 1

    requirement = requirements[0]

    assert requirement.skill_name == "Python"
    assert requirement.required_proficiency is None
    assert requirement.required_years_experience is None