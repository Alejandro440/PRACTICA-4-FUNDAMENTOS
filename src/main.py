"""Entry point for the PEC4 project."""
from __future__ import annotations

import argparse
from pathlib import Path

from src.modules.analysis import analyze_dataset
from src.modules.cleaning import prepare_datasets
from src.modules.data_loading import explore_dataset, load_dataset
from src.modules.visualization import plot_time_series


def run_exercise_1(data_dir: Path, dataset_path: Path | None = None) -> None:
    """Run exercise 1 (load and EDA)."""
    df = load_dataset(dataset_path, data_dir=data_dir)
    explore_dataset(df)


def run_exercise_2(data_dir: Path) -> Path:
    """Run exercise 2 (clean, aggregate, merge)."""
    rendiment_df = load_dataset(data_dir / "rendiment_estudiants.xlsx")
    abandono_df = load_dataset(data_dir / "taxa_abandonament.xlsx")
    merged_df = prepare_datasets(rendiment_df, abandono_df)
    output_path = data_dir / "src" / "report" / "merged_dataset.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    merged_df.to_csv(output_path, index=False)
    print(f"Dataset fusionado guardado en: {output_path}")
    return output_path


def run_exercise_3(data_dir: Path) -> Path:
    """Run exercise 3 (visualization)."""
    rendiment_df = load_dataset(data_dir / "rendiment_estudiants.xlsx")
    abandono_df = load_dataset(data_dir / "taxa_abandonament.xlsx")
    merged_df = prepare_datasets(rendiment_df, abandono_df)
    output_path = data_dir / "src" / "img" / "evolucion_nombre_alumno.png"
    plot_time_series(merged_df, output_path)
    print(f"Gráfico guardado en: {output_path}")
    return output_path


def run_exercise_4(data_dir: Path) -> Path:
    """Run exercise 4 (statistical analysis)."""
    rendiment_df = load_dataset(data_dir / "rendiment_estudiants.xlsx")
    abandono_df = load_dataset(data_dir / "taxa_abandonament.xlsx")
    merged_df = prepare_datasets(rendiment_df, abandono_df)
    output_path = data_dir / "src" / "report" / "analisi_estadistic.json"
    analyze_dataset(merged_df, output_path)
    print(f"Informe guardado en: {output_path}")
    return output_path


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Proyecto PEC4: Rendimiento de estudiantes universitarios"
    )
    parser.add_argument(
        "-ex",
        "--exercise",
        type=int,
        choices=[1, 2, 3, 4],
        help=(
            "Ejecuta ejercicios de forma progresiva hasta el número indicado. "
            "Ejemplo: -ex 3 ejecuta del 1 al 3."
        ),
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        help="Ruta opcional para el dataset en el ejercicio 1.",
    )
    return parser.parse_args()


def main() -> None:
    """Main execution function."""
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]

    exercise_limit = args.exercise or 4

    if exercise_limit >= 1:
        run_exercise_1(repo_root, args.dataset)
    if exercise_limit >= 2:
        run_exercise_2(repo_root)
    if exercise_limit >= 3:
        run_exercise_3(repo_root)
    if exercise_limit >= 4:
        run_exercise_4(repo_root)


if __name__ == "__main__":
    main()
