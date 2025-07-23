import os
import pandas as pd
import unicodedata

def normalizar_nombre(nombre):
    nombre = nombre.lower().strip().replace(" ", "_").replace(".", "")
    nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('utf-8')
    return nombre

def obtener_tipo_estacion_por_codigo(empresa, codigo_estacion, ruta_base="./data"):
    """
    Devuelve el tipo de trampa según el código ingresado y la empresa seleccionada.
    También valida si el código existe en el archivo.
    """
    carpeta_normalizada = normalizar_nombre(empresa)

    # Buscar carpeta coincidente
    for carpeta in os.listdir(ruta_base):
        if normalizar_nombre(carpeta) == carpeta_normalizada:
            ruta_archivo = os.path.join(ruta_base, carpeta, "codes.xlsx")
            break
    else:
        print(f"[ERROR] Carpeta no encontrada para empresa '{empresa}'")
        return None

    if not os.path.isfile(ruta_archivo):
        print(f"[ERROR] No se encontró el archivo: {ruta_archivo}")
        return None

    try:
        df = pd.read_excel(ruta_archivo)

        fila = df[df["Codigo"] == codigo_estacion]
        if fila.empty:
            print(f"[ERROR] El código {codigo_estacion} no está definido en el archivo de la empresa '{empresa}'")
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

    return None