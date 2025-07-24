# utils/codigo_estaciones.py

import pandas as pd
import unicodedata
from utils.rutas import get_codes_path


def normalizar_nombre(nombre):
    nombre = nombre.lower().strip().replace(" ", "_").replace(".", "")
    nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('utf-8')
    return nombre


def obtener_tipo_estacion_por_codigo(empresa, codigo_estacion):
    """
    Devuelve el tipo de trampa según el código ingresado y la empresa seleccionada.
    """
    try:
        path = get_codes_path(empresa)
        if not path.exists():
            print(f"[ERROR] No se encontró el archivo: {path}")
            return None

        df = pd.read_excel(path)

        fila = df[df["Codigo"] == codigo_estacion]
        if fila.empty:
            print(f"[ERROR] El código {codigo_estacion} no está definido en {path}")
            return None

        tipo_raw = str(fila.iloc[0]["Tipo de trampa"]).strip().lower()
        if "quimico" in tipo_raw:
            return "Cebadero Químico"
        elif "pegamentosa" in tipo_raw:
            return "Planchas Pegamentosas"
        elif "jaula" in tipo_raw:
            return "Trampa Jaulas"
        else:
            return tipo_raw.title()

    except Exception as e:
        print(f"[ERROR] Falló la lectura de codes.xlsx: {e}")
        return None
