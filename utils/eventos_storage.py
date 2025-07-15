# utils/eventos_storage.py

import json

FILENAME = "eventos_temp.json"

def guardar_evento(numero, evento, observacion):
    nuevo = {"numero": numero, "evento": evento, "observacion": observacion}
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            eventos = json.load(f)
    except FileNotFoundError:
        eventos = []

    eventos.append(nuevo)

    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(eventos, f, indent=4)

def cargar_eventos():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def limpiar_eventos():
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump([], f)
