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


def test_female_opponent_age_is_derived_from_birth_date(female_rows):
    dates = _to_date([row[0] for row in female_rows])
    ages = _opponent_ages(female_rows, dates, male=False)
    assert ages[0] == pytest.approx(18.776, abs=1e-3)


def test_male_opponent_age_is_read_directly(male_rows):
    dates = _to_date([row[0] for row in male_rows])
    ages = _opponent_ages(male_rows, dates, male=True)
    assert list(ages) == pytest.approx([22.264202601, 24.2902121834, 18.7597535934])


def test_clean_matches_female(female_rows):
    matches = _clean_matches(female_rows, "19810926")
    assert list(matches.columns) == [
        "match_date", "opponent", "result", "player_age", "opponent_age", "age_diff"]
    assert list(matches["result"]) == ["loss", "loss", "loss"]
    assert matches["age_diff"][0] == pytest.approx(-4.684, abs=1e-3)


def test_clean_matches_male(male_rows):
    matches = _clean_matches(male_rows, "19860603")
    assert sorted(matches["result"]) == ["loss", "loss", "win"]
    assert matches["player_age"][0] == pytest.approx(15.272, abs=1e-3)
    assert matches["age_diff"][0] == pytest.approx(-6.992, abs=1e-3)
