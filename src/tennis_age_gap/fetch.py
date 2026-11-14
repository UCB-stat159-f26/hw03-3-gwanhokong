"""Download raw career and player files from tennisabstract.com."""

import time

import requests

from .clean import _parse_dob

BASE_URL = "https://www.tennisabstract.com"
TIMEOUT_SECONDS = 30
HEADERS = {"User-Agent": "tennis_age_gap (STAT 159 HW3 student package)"}
RETRY_WAITS = (5, 15, 30)  # seconds to wait after each HTTP 429 response


def _normalize_name(player_name):
    """'serena williams', 'Serena Williams' or 'SerenaWilliams' -> 'SerenaWilliams'."""
    words = str(player_name).split()
    if not words:
        raise ValueError("player_name must be a non-empty string, e.g. 'Serena Williams'")
    return "".join(word[0].upper() + word[1:] for word in words)


def _get_text(url):
    """Return the text at `url`, or None if the page does not exist (HTTP 404).

    tennisabstract.com answers 429 (Too Many Requests) when asked too often,
    so wait and try again a few times before giving up.
    """
    for wait in (*RETRY_WAITS, None):
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
        if response.status_code != 429 or wait is None:
            break
        time.sleep(wait)
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


def _fetch_player_dob(slug, male):
    """Download the player page (men: player.cgi, women: wplayer.cgi) and read the birth date."""
    page = "player.cgi" if male else "wplayer.cgi"
    dob = _parse_dob(_get_text(f"{BASE_URL}/cgi-bin/{page}?p={slug}") or "")
    if dob is None:
        raise ValueError(f"Could not find a birth date for '{slug}' on tennisabstract.com.")
    return dob
