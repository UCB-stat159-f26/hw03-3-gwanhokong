"""Tests for parsing and cleaning career JS files (no network access)."""

from pathlib import Path

import pytest

from tennis_age_gap.clean import (
    _clean_matches, _is_male_format, _opponent_ages,
    _parse_dob, _parse_matches_js, _to_date,
)

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def female_rows():
    return _parse_matches_js((DATA_DIR / "FemalePlayerCareer.js").read_text())


@pytest.fixture
def male_rows():
    return _parse_matches_js((DATA_DIR / "MalePlayerCareer.js").read_text())


def test_parse_matches_js_returns_all_rows(female_rows, male_rows):
    assert len(female_rows) == 3 and len(male_rows) == 3
    assert female_rows[0][0] == "19951030"
    assert male_rows[2][11] == "Israel Matos Gil"


def test_is_male_format(female_rows, male_rows):
    assert not _is_male_format(female_rows)
    assert _is_male_format(male_rows)


def test_parse_dob():
    assert _parse_dob("var fullname = 'X';\nvar dob = 19810926;") == "19810926"
    assert _parse_dob("<html>no birth date here</html>") is None
