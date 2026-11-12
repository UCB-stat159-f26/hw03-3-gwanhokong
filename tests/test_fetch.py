"""Tests for player-name handling and error messages (no network access)."""

import pytest

from tennis_age_gap import fetch


@pytest.mark.parametrize(
    "name", ["serena williams", "Serena Williams", "SerenaWilliams", "  serena   williams "])
def test_normalize_name_accepts_common_spellings(name):
    assert fetch._normalize_name(name) == "SerenaWilliams"


def test_normalize_name_rejects_empty_input():
    with pytest.raises(ValueError):
        fetch._normalize_name("   ")


def test_unknown_player_gives_meaningful_error(monkeypatch):
    monkeypatch.setattr(fetch, "_get_text", lambda url: None)  # pretend the server said 404
    with pytest.raises(ValueError, match="No career data found for 'GastonSanchez'"):
        fetch._fetch_career_js("GastonSanchez")
