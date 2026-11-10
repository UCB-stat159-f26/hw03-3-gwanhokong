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
