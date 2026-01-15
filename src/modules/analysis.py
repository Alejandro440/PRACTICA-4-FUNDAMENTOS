"""Statistical analysis utilities."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
from scipy.stats import linregress, pearsonr


def analyze_dataset(merged_df: pd.DataFrame, output_path: Path) -> dict:
    """Generate a statistical analysis report and save it to JSON.

    Args:
        merged_df: Cleaned and merged dataframe.
        output_path: Output path for the JSON report.

    Returns:
        Dictionary containing the analysis results.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    corr, _p_value = pearsonr(
        merged_df["% Abandonament a primer curs"].dropna(),
        merged_df["Taxa rendiment"].dropna(),
    )

    analysis = {
        "metadata": {
            "fecha_analisis": datetime.now().strftime("%Y-%m-%d"),
            "num_registros": len(merged_df),
            "periodo_temporal": sorted(merged_df["Curs Acadèmic"].unique().tolist()),
        },
        "estadisticas_globales": {
            "abandono_medio": merged_df["% Abandonament a primer curs"].mean(),
            "rendimiento_medio": merged_df["Taxa rendiment"].mean(),
            "correlacion_abandono_rendimiento": corr,
        },
        "analisis_por_rama": {},
        "rankings": {},
    }

    for branch in sorted(merged_df["Branca"].dropna().unique()):
        branch_data = merged_df[merged_df["Branca"] == branch]
        abandonment_mean = branch_data["% Abandonament a primer curs"].mean()
        abandonment_std = branch_data["% Abandonament a primer curs"].std()
        performance_mean = branch_data["Taxa rendiment"].mean()
        performance_std = branch_data["Taxa rendiment"].std()

        branch_by_year = (
            branch_data.groupby("Curs Acadèmic")["% Abandonament a primer curs"]
            .mean()
            .reset_index()
        )
        years = branch_by_year["Curs Acadèmic"].tolist()
        valores_abandono = branch_by_year["% Abandonament a primer curs"].tolist()
        if len(years) > 1:
            slope, _intercept, _r_value, _p_val, _std_err = linregress(
                range(len(years)), valores_abandono
            )
        else:
            slope = 0.0

        if slope > 0.01:
            tendencia = "creciente"
        elif slope < -0.01:
            tendencia = "decreciente"
        else:
            tendencia = "estable"

        analysis["analisis_por_rama"][branch] = {
            "abandono_media": abandonment_mean,
            "abandono_std": abandonment_std,
            "rendimiento_media": performance_mean,
            "rendimiento_std": performance_std,
            "tendencia_abandono": tendencia,
            "pendiente_abandono": slope,
        }

    rankings_df = merged_df.groupby("Branca").agg(
        abandono_media=("% Abandonament a primer curs", "mean"),
        rendimiento_media=("Taxa rendiment", "mean"),
    )
    rankings_df = rankings_df.dropna()
    analysis["rankings"] = {
        "mejor_rendimiento": rankings_df["rendimiento_media"].idxmax(),
        "peor_rendimiento": rankings_df["rendimiento_media"].idxmin(),
        "mayor_abandono": rankings_df["abandono_media"].idxmax(),
        "menor_abandono": rankings_df["abandono_media"].idxmin(),
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(analysis, file, ensure_ascii=False, indent=2)

    return analysis
