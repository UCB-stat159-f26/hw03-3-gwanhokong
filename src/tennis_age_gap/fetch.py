"""Download raw career and player files from tennisabstract.com."""

import requests

from .clean import _parse_dob

BASE_URL = "https://www.tennisabstract.com"
TIMEOUT_SECONDS = 30


def _normalize_name(player_name):
    """'serena williams', 'Serena Williams' or 'SerenaWilliams' -> 'SerenaWilliams'."""
    words = str(player_name).split()
    if not words:
        raise ValueError("player_name must be a non-empty string, e.g. 'Serena Williams'")
    return "".join(word[0].upper() + word[1:] for word in words)


def _get_text(url):
    """Return the text at `url`, or None if the page does not exist (HTTP 404)."""
    response = requests.get(url, timeout=TIMEOUT_SECONDS)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.text


def _fetch_career_js(slug):
    """Download the career JS file of a player, failing clearly if it does not exist."""
    js_text = _get_text(f"{BASE_URL}/jsmatches/{slug}Career.js")
    if js_text is None:
        raise ValueError(
            f"No career data found for '{slug}' on tennisabstract.com. "
            "Check the spelling of the player's name, e.g. 'Serena Williams'."
        )
    return js_text
