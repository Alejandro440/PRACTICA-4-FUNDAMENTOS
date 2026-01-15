# PEC4 - Rendimiento de estudiantes universitarios en Cataluña

Este proyecto resuelve la PEC4 de **Programación para la ciencia de datos**. Se trabaja con dos datasets en formato Excel:

- `rendiment_estudiants.xlsx` (tasa de rendimiento)
- `taxa_abandonament.xlsx` (tasa de abandono)

El código está organizado en módulos y permite ejecutar los ejercicios de forma progresiva desde `main.py`.

## Estructura del proyecto

```
.
├── src/
│   ├── main.py
│   ├── modules/
│   │   ├── analysis.py
│   │   ├── cleaning.py
│   │   ├── data_loading.py
│   │   └── visualization.py
│   ├── img/
│   └── report/
├── tests/
├── examples/
├── doc/
├── screenshots/
├── rendiment_estudiants.xlsx
├── taxa_abandonament.xlsx
├── requirements.txt
└── LICENSE
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

Ejecutar todos los ejercicios:

```bash
python src/main.py
```

Ejecutar ejercicios de forma progresiva (por ejemplo, hasta el 3):

```bash
python src/main.py -ex 3
```

Ejercicio 1 con dataset específico:

```bash
python src/main.py -ex 1 --dataset rendiment_estudiants.xlsx
```

## Resultados

- Dataset fusionado: `src/report/merged_dataset.csv`
- Informe estadístico: `src/report/analisi_estadistic.json`
- Gráfico: `src/img/evolucion_nombre_alumno.png`

## Documentación (HTML)

Se puede generar la documentación HTML a partir de docstrings con `pydoc`:

```bash
python -m pydoc -w src.modules.data_loading src.modules.cleaning src.modules.visualization src.modules.analysis
mkdir -p doc
mv data_loading.html cleaning.html visualization.html analysis.html doc/
```

## Tests y cobertura

Para ejecutar los tests:

```bash
pytest
```

Para cobertura (requiere `pytest-cov`):

```bash
pytest --cov=src --cov-report=term-missing
```

## Linter

Se recomienda `pylint` para verificar estilo:

```bash
pylint src/modules src/main.py
```

## Capturas de pantalla

Las capturas solicitadas deben guardarse en la carpeta `screenshots/`.
