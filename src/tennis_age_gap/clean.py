"""Parse and clean tennisabstract.com career files (no network access)."""

import json
import re

import pandas as pd

# Positions of the fields we use inside each match row
DATE_COL, RESULT_COL, OPPONENT_COL, OPP_AGE_COL = 0, 4, 11, 16


def _parse_matches_js(js_text):
    """Turn the text `var morematchmx = [[...], ...];` into a list of rows."""
    body = re.sub(r"^\s*var\s+\w+\s*=\s*", "", js_text)
    body = re.sub(r";\s*$", "", body)
    return json.loads(body)


def _is_male_format(rows):
    """Male files store opponent age as a decimal ('22.26'); female files store a birth date."""
    return any("." in row[OPP_AGE_COL] for row in rows)


def _parse_dob(page_html):
    """Extract the player's birth date ('YYYYMMDD') from a player page, or None."""
    match = re.search(r"var dob\s*=\s*(\d{8})\s*;", page_html)
    return match.group(1) if match else None


def _to_date(values):
    """Convert 'YYYYMMDD' strings to dates; invalid or empty values become NaT."""
    return pd.Series(pd.to_datetime(values, format="%Y%m%d", errors="coerce"))


def _years_between(start, end):
    """Elapsed time in years between two dates (works element-wise on Series)."""
    return (end - start).dt.days / 365.25


def _opponent_ages(rows, match_dates, male):
    """Opponent age in years: given directly in male files, derived from birth date in female files."""
    raw = pd.Series([row[OPP_AGE_COL] for row in rows])
    if male:
        return pd.to_numeric(raw, errors="coerce")
    return _years_between(_to_date(raw), match_dates)
