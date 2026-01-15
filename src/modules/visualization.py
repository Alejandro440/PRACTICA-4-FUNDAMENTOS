"""Visualization utilities for the analysis."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_time_series(merged_df: pd.DataFrame, output_path: Path) -> Path:
    """Generate time-series plots for abandonment and performance.

    Args:
        merged_df: Cleaned and merged dataframe.
        output_path: Output file path for the generated figure.

    Returns:
        Path to the saved figure.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    branches = sorted(merged_df["Branca"].dropna().unique())
    years = sorted(merged_df["Curs Acadèmic"].dropna().unique())
    colors = plt.cm.tab10.colors

    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

    for idx, branch in enumerate(branches):
        branch_df = merged_df[merged_df["Branca"] == branch]
        abandonment_by_year = (
            branch_df.groupby("Curs Acadèmic")["% Abandonament a primer curs"]
            .mean()
            .reindex(years)
        )
        performance_by_year = (
            branch_df.groupby("Curs Acadèmic")["Taxa rendiment"]
            .mean()
            .reindex(years)
        )
        color = colors[idx % len(colors)]
        axes[0].plot(years, abandonment_by_year, label=branch, color=color)
        axes[1].plot(years, performance_by_year, label=branch, color=color)

    axes[0].set_title("Evolución del % de abandono por curso académico")
    axes[0].set_ylabel("% Abandonament a primer curs")
    axes[0].grid(True)
    axes[0].legend(loc="best")

    axes[1].set_title("Evolución de la tasa de rendimiento por curso académico")
    axes[1].set_xlabel("Curs Acadèmic")
    axes[1].set_ylabel("Taxa rendiment")
    axes[1].grid(True)
    axes[1].legend(loc="best")

    plt.xticks(rotation=45)
    plt.tight_layout()
    fig.savefig(output_path, dpi=300)
    plt.close(fig)

    return output_path
