# utils/rutas.py

from pathlib import Path

APP_NAME = "srd_app"

# Carpeta base donde se guarda todo (ej: C:\Users\<usuario>\.srd_app)
BASE_DIR = Path.home() / f".{APP_NAME}"
BASE_DIR.mkdir(parents=True, exist_ok=True)


def get_base_dir():
    """Devuelve la ruta base para almacenamiento permanente"""
    return BASE_DIR


def get_temp_file(nombre="eventos_temp.json"):
    """Ruta al archivo temporal de eventos"""
    return BASE_DIR / nombre


def get_user_file():
    """Ruta al archivo de usuarios"""
    return BASE_DIR / "users.json"


def get_remember_file():
    """Ruta al archivo de recordarme"""
    return BASE_DIR / "remember.json"


def get_data_folder(empresa):
    """Carpeta para datos de una empresa específica"""
    folder = BASE_DIR / "data" / empresa
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_codes_path(empresa):
    """Archivo codes.xlsx de una empresa"""
    return get_data_folder(empresa) / "codes.xlsx"


def get_export_path(empresa, nombre_archivo):
    """Archivo de exportación (ej: revision_empresa_fecha.xlsx)"""
    return get_data_folder(empresa) / nombre_archivo
