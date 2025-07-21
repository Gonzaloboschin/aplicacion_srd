import pandas as pd
import os
from pathlib import Path
from datetime import date

BASE_DIR = Path(__file__).parent.parent / "data"

def ensure_company_folder(empresa):
    """Crea la carpeta data/<empresa> si no existe."""
    folder = BASE_DIR / empresa
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def load_codes(empresa):
    """Lee data/<empresa>/codes.xlsx y devuelve un DataFrame."""
    folder = ensure_company_folder(empresa)
    codes_path = folder / "codes.xlsx"
    if not codes_path.exists():
        raise FileNotFoundError(f"No existe el archivo de códigos en {codes_path}")
    return pd.read_excel(codes_path, dtype={"station_number": str, "trap_type": str})

def export_revision(empresa, eventos):
    """
    Recibe lista de dicts con claves
    numero, tipo_estacion, tipo_evento, observacion
    y genera revision_{empresa}_{YYYYMMDD}.xlsx en la carpeta de la empresa.
    """
    folder = ensure_company_folder(empresa)
    hoy = date.today().strftime("%Y%m%d")
    filename = f"revision_{empresa.lower().replace(' ', '_')}_{hoy}.xlsx"
    path = folder / filename

    # Crear DataFrame y volcar a Excel
    df = pd.DataFrame(eventos)
    # Asegurarse del orden de columnas:
    df = df[["numero", "tipo_estacion", "tipo_evento", "observacion"]]
    df.to_excel(path, index=False, engine="openpyxl")
    return path
