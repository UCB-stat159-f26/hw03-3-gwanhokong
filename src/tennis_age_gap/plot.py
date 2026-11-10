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


def _age_ticks(age_diff):
    """Y ticks every 10 years covering the data, with 0 labeled 'Same age'."""
    low = int(age_diff.min() // 10) * 10
    high = int(-(-age_diff.max() // 10)) * 10
    ticks = list(range(low, high + 1, 10))
    labels = ["Same age" if tick == 0 else f"{tick:+d}" for tick in ticks]
    return ticks, labels


def _style_axes(ax, age_diff):
    """NYT-like axes: age on top, 'Same age' baseline, light grid, no box."""
    ax.set_xlabel("Player's age")
    ax.set_ylabel("Age difference with opponent (years)\n"
                  "Younger than opponent  <-  ->  Older than opponent")
    ax.set_yticks(*_age_ticks(age_diff))
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position("top")
    ax.grid(color="0.9")
    ax.set_axisbelow(True)
    for side in ("right", "bottom"):
        ax.spines[side].set_visible(False)
