# main.py

from auth.login_window import show_login
from ui.operario_ui import abrir_interfaz_operario
# from ui.admin_ui import abrir_interfaz_admin  # ← para cuando esté lista la interfaz de administrador

def main():
    session = show_login()

    if session["username"]:
        rol = session["role"].lower()

        if rol in ["operario", "user"]:
            abrir_interfaz_operario(session["username"])
        elif rol == "admin":
            print("Funcionalidad de administrador próximamente disponible.")
            # abrir_interfaz_admin(session["username"])
        else:
            print(f"Rol no manejado aún: '{rol}'")
    else:
        print("Login fallido o cancelado.")

if __name__ == "__main__":
    main()
