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


class FakeResponse:
    """Minimal stand-in for requests.Response."""

    def __init__(self, status_code, text=""):
        self.status_code = status_code
        self.text = text

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


def test_get_text_retries_after_too_many_requests(monkeypatch):
    responses = iter([FakeResponse(429), FakeResponse(200, "var dob = 19810926;")])
    monkeypatch.setattr(fetch.requests, "get", lambda url, **kwargs: next(responses))
    monkeypatch.setattr(fetch.time, "sleep", lambda seconds: None)  # do not really wait
    assert fetch._get_text("https://example.com") == "var dob = 19810926;"
