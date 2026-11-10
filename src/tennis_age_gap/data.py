"""Public function that downloads and cleans a player's career matches."""

from .clean import _clean_matches, _is_male_format, _parse_matches_js
from .fetch import _fetch_career_js, _fetch_player_dob, _normalize_name


def get_career_matches(player_name):
    """Get a player's career matches from tennisabstract.com as a clean data frame.

    player_name: e.g. "serena williams", "Serena Williams" or "SerenaWilliams".
    Returns columns: match_date, opponent, result, player_age, opponent_age, age_diff.
    Raises ValueError if the player cannot be found on tennisabstract.com.
    """
    slug = _normalize_name(player_name)
    rows = _parse_matches_js(_fetch_career_js(slug))
    dob = _fetch_player_dob(slug, _is_male_format(rows))
    return _clean_matches(rows, dob)
