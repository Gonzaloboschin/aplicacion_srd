# utils/excel_storage.py

import pandas as pd
from datetime import date
from pathlib import Path
from utils.rutas import get_codes_path

def load_codes(empresa):
    """
    Carga el archivo codes.xlsx de la empresa.
    """
    path = get_codes_path(empresa)
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo de códigos en {path}")
    return pd.read_excel(path, dtype={"station_number": str, "trap_type": str})


def export_revision(empresa, eventos):
    """
    Exporta la revisión a un archivo Excel en la misma carpeta donde se ejecuta la app.
    """
    hoy = date.today().strftime("%Y%m%d")
    filename = f"revision_{empresa.lower().replace(' ', '_')}_{hoy}.xlsx"
    output_path = Path.cwd() / filename

    df = pd.DataFrame(eventos)
    df = df[["numero", "tipo_estacion", "tipo_evento", "observacion"]]
    df.to_excel(output_path, index=False, engine="openpyxl")

    return output_path
