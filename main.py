# main.py

from auth.login_window import show_login
from ui.operario_ui import abrir_interfaz_operario


session = show_login()

if session["username"]:
    rol = session["role"]

    if rol == "operario":
        abrir_interfaz_operario(session["username"])
    else:
        print(f"Rol no manejado aún: {rol}")
else:
    print("Login fallido o cancelado.")
