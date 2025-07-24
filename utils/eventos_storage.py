# utils/eventos_storage.py

import json
from utils.rutas import get_temp_file

# Ruta fija al archivo temporal de eventos (dentro de ~/.srd_app/)
FILENAME = get_temp_file("eventos_temp.json")

def guardar_evento(numero, tipo_estacion, tipo_evento, observacion):
    nuevo = {
        "numero": numero,
        "tipo_estacion": tipo_estacion,
        "tipo_evento": tipo_evento,
        "observacion": observacion
    }
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            eventos = json.load(f)
    except FileNotFoundError:
        eventos = []

    eventos.append(nuevo)

    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=4, ensure_ascii=False)


def cargar_eventos():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def limpiar_eventos():
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump([], f)
