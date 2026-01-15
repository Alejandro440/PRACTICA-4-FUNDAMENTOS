import pandas as pd

from src.modules.cleaning import (
    GROUP_COLUMNS,
    merge_datasets,
    prepare_datasets,
    standardize_columns,
)


def test_standardize_columns_renames():
    df = pd.DataFrame({"Curs Academic": ["2020-2021"], "Taxa rendiment": [90]})
    standardized = standardize_columns(df)
    assert "Curs Acadèmic" in standardized.columns


def test_prepare_datasets_merges():
    rendiment_df = pd.DataFrame(
        {
            "Curs Acadèmic": ["2020-2021", "2020-2021"],
            "Tipus universitat": ["Pública", "Pública"],
            "Sigles": ["UNI", "UNI"],
            "Tipus Estudi": ["Grau", "Grau"],
            "Branca": ["Ciències", "Ciències"],
            "Sexe": ["D", "D"],
            "Integrat S/N": ["S", "S"],
            "Taxa rendiment": [80, 90],
        }
    )
    abandono_df = pd.DataFrame(
        {
            "Curs Acadèmic": ["2020-2021", "2020-2021"],
            "Tipus universitat": ["Pública", "Pública"],
            "Sigles": ["UNI", "UNI"],
            "Tipus Estudi": ["Grau", "Grau"],
            "Branca": ["Ciències", "Ciències"],
            "Sexe": ["D", "D"],
            "Integrat S/N": ["S", "S"],
            "% Abandonament a primer curs": [10, 12],
        }
    )
    merged = prepare_datasets(rendiment_df, abandono_df)
    assert list(merged.columns) == GROUP_COLUMNS + ["Taxa rendiment", "% Abandonament a primer curs"]
    assert merged["Taxa rendiment"].iloc[0] == 85
    assert merged["% Abandonament a primer curs"].iloc[0] == 11


def test_merge_datasets_inner():
    rendiment_df = pd.DataFrame(
        {
            "Curs Acadèmic": ["2020-2021"],
            "Tipus universitat": ["Pública"],
            "Sigles": ["UNI"],
            "Tipus Estudi": ["Grau"],
            "Branca": ["Ciències"],
            "Sexe": ["D"],
            "Integrat S/N": ["S"],
            "Taxa rendiment": [85],
        }
    )
    abandono_df = pd.DataFrame(
        {
            "Curs Acadèmic": ["2020-2021"],
            "Tipus universitat": ["Pública"],
            "Sigles": ["UNI"],
            "Tipus Estudi": ["Grau"],
            "Branca": ["Ciències"],
            "Sexe": ["D"],
            "Integrat S/N": ["S"],
            "% Abandonament a primer curs": [11],
        }
    )
    merged = merge_datasets(rendiment_df, abandono_df)
    assert len(merged) == 1
