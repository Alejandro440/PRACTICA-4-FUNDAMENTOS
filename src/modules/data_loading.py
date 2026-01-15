"""Data loading and exploratory analysis utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


DATASETS = {
    "1": "rendiment_estudiants.xlsx",
    "2": "taxa_abandonament.xlsx",
}


def load_dataset(file_path: Optional[Path] = None, data_dir: Optional[Path] = None) -> pd.DataFrame:
    """Load a dataset from the provided path or by prompting the user.

    Args:
        file_path: Optional path to the dataset.
        data_dir: Optional directory containing the datasets.

    Returns:
        Loaded pandas DataFrame.

    Raises:
        FileNotFoundError: If the provided path does not exist.
        ValueError: If the user selection is invalid.
    """
    if file_path is None:
        data_dir = data_dir or Path.cwd()
        print("Selecciona el dataset a cargar:")
        print("1 - Tasa de rendimiento (rendiment_estudiants.xlsx)")
        print("2 - Tasa de abandono (taxa_abandonament.xlsx)")
        choice = input("Introduce 1 o 2: ").strip()
        if choice not in DATASETS:
            raise ValueError("Selección inválida. Debes escoger 1 o 2.")
        file_path = data_dir / DATASETS[choice]

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"No se encuentra el fichero: {file_path}")

    return pd.read_excel(file_path)


def explore_dataset(df: pd.DataFrame) -> None:
    """Print basic EDA information for a dataframe.

    Args:
        df: DataFrame to explore.
    """
    print("\nPrimeras 5 filas:")
    print(df.head())
    print("\nColumnas:")
    print(df.columns)
    print("\nInformación del dataframe:")
    df.info()
