"""Cleaning and merging utilities for the datasets."""
from __future__ import annotations

from typing import Iterable, List

import pandas as pd


CANONICAL_COLUMNS = {
    "curs acadèmic": "Curs Acadèmic",
    "curs academic": "Curs Acadèmic",
    "tipus universitat": "Tipus universitat",
    "universitat": "Universitat",
    "unitat": "Unitat",
    "sigles": "Sigles",
    "tipus estudi": "Tipus Estudi",
    "tipus estudis": "Tipus Estudi",
    "branca": "Branca",
    "sexe": "Sexe",
    "integrat s/n": "Integrat S/N",
    "integrat sn": "Integrat S/N",
    "crèdits ordinaris superats": "Crèdits ordinaris superats",
    "credits ordinaris superats": "Crèdits ordinaris superats",
    "crèdits ordinaris matriculats": "Crèdits ordinaris matriculats",
    "credits ordinaris matriculats": "Crèdits ordinaris matriculats",
    "% abandonament a primer curs": "% Abandonament a primer curs",
    "taxa rendiment": "Taxa rendiment",
}

GROUP_COLUMNS = [
    "Curs Acadèmic",
    "Tipus universitat",
    "Sigles",
    "Tipus Estudi",
    "Branca",
    "Sexe",
    "Integrat S/N",
]


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to a canonical set.

    Args:
        df: DataFrame to standardize.

    Returns:
        DataFrame with standardized column names.
    """
    rename_map = {}
    for column in df.columns:
        key = column.strip().lower()
        if key in CANONICAL_COLUMNS:
            rename_map[column] = CANONICAL_COLUMNS[key]
    return df.rename(columns=rename_map)


def drop_unnecessary_columns(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Drop columns if they exist in the dataframe.

    Args:
        df: DataFrame to clean.
        columns: Iterable of columns to drop.

    Returns:
        Cleaned DataFrame.
    """
    existing = [col for col in columns if col in df.columns]
    return df.drop(columns=existing)


def _ensure_columns(df: pd.DataFrame, columns: List[str]) -> None:
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")


def group_by_branch(df: pd.DataFrame, value_column: str) -> pd.DataFrame:
    """Group by branch and compute mean for the requested metric.

    Args:
        df: Input dataframe.
        value_column: Metric column to aggregate.

    Returns:
        Aggregated dataframe.
    """
    _ensure_columns(df, GROUP_COLUMNS + [value_column])
    grouped = (
        df.groupby(GROUP_COLUMNS, as_index=False)[value_column]
        .mean()
        .rename(columns={value_column: value_column})
    )
    return grouped


def merge_datasets(rendiment_df: pd.DataFrame, abandono_df: pd.DataFrame) -> pd.DataFrame:
    """Merge datasets using shared keys (inner merge).

    Args:
        rendiment_df: Aggregated rendimiento dataframe.
        abandono_df: Aggregated abandono dataframe.

    Returns:
        Merged dataframe containing matching rows.
    """
    _ensure_columns(rendiment_df, GROUP_COLUMNS + ["Taxa rendiment"])
    _ensure_columns(abandono_df, GROUP_COLUMNS + ["% Abandonament a primer curs"])
    merged = pd.merge(rendiment_df, abandono_df, on=GROUP_COLUMNS, how="inner")
    return merged


def prepare_datasets(
    rendiment_df: pd.DataFrame, abandono_df: pd.DataFrame
) -> pd.DataFrame:
    """Clean, aggregate, and merge the provided datasets.

    Args:
        rendiment_df: Raw rendimiento dataset.
        abandono_df: Raw abandono dataset.

    Returns:
        Merged dataframe ready for analysis.
    """
    rendiment_df = standardize_columns(rendiment_df)
    abandono_df = standardize_columns(abandono_df)

    common_drop = ["Universitat", "Unitat"]
    rendiment_df = drop_unnecessary_columns(
        rendiment_df,
        common_drop + ["Crèdits ordinaris superats", "Crèdits ordinaris matriculats"],
    )
    abandono_df = drop_unnecessary_columns(abandono_df, common_drop)

    rendiment_grouped = group_by_branch(rendiment_df, "Taxa rendiment")
    abandono_grouped = group_by_branch(abandono_df, "% Abandonament a primer curs")

    return merge_datasets(rendiment_grouped, abandono_grouped)
