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
