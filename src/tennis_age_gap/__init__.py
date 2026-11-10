"""Tennis career matches and age-gap plots from tennisabstract.com."""

from .data import get_career_matches
from .plot import plot_age_gap

__all__ = ["get_career_matches", "plot_age_gap"]
