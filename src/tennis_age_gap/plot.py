"""Public function that draws the NYT-style age-gap scatter plot."""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

COLORS = {"win": "#4FC3E8", "loss": "#7B2D8E"}
LABELS = {"win": "Match won", "loss": "Match lost"}


def _draw_points(ax, matches):
    """Scatter the matches, drawing losses last so they are not hidden behind wins."""
    ordered = matches.sort_values("result", key=lambda col: col == "loss", kind="stable")
    ax.axhline(0, color="gray", linewidth=0.8, zorder=1)
    ax.scatter(ordered["player_age"], ordered["age_diff"],
               c=ordered["result"].map(COLORS), s=14, alpha=0.75, zorder=2)
