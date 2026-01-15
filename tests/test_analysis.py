import pandas as pd

from src.modules.analysis import analyze_dataset


def test_analyze_dataset_creates_report(tmp_path):
    merged_df = pd.DataFrame(
        {
            "Curs Acadèmic": ["2020-2021", "2021-2022"],
            "Tipus universitat": ["Pública", "Pública"],
            "Sigles": ["UNI", "UNI"],
            "Tipus Estudi": ["Grau", "Grau"],
            "Branca": ["Ciències", "Ciències"],
            "Sexe": ["D", "D"],
            "Integrat S/N": ["S", "S"],
            "Taxa rendiment": [85, 87],
            "% Abandonament a primer curs": [11, 9],
        }
    )
    output_path = tmp_path / "analysis.json"
    report = analyze_dataset(
        merged_df,
        output_path,
        student_name="Alejandro Alonso Anda",
        student_id="alejandro_alonso_anda",
        source_files=["rendiment_estudiants.xlsx", "taxa_abandonament.xlsx"],
    )

    assert output_path.exists()
    assert "metadata" in report
    assert "estadisticas_globales" in report
    assert "analisis_por_rama" in report
    assert "rankings" in report
