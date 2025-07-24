# ui/menu_operario.py

import tkinter as tk
from tkinter import messagebox
from ui.cargar_evento_ui import abrir_cargar_evento
from ui.revision_final_ui import revision_final_operario


def centrar_ventana(ventana, ancho=800, alto=600):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.resizable(False, False)


def menu_operario(nombre_usuario, empresa, volver_func):
    
    def cargar_evento():
        ventana.destroy()
        abrir_cargar_evento(nombre_usuario, empresa, lambda: menu_operario(nombre_usuario, empresa, volver_func))

    def modificar_evento():
        ventana.destroy()
        revision_final_operario(nombre_usuario, empresa,
                                lambda: menu_operario(nombre_usuario, empresa, volver_func))

    def eliminar_evento():
        ventana.destroy()
        revision_final_operario(nombre_usuario, empresa,
                                lambda: menu_operario(nombre_usuario, empresa, volver_func))


    def salir():
        messagebox.showinfo("Sesión finalizada", "La revisión fue completada. Volviendo al inicio.")
        ventana.destroy()
        volver_func()

    ventana = tk.Tk()
    ventana.title("Menú del Operario")
    centrar_ventana(ventana)
    ventana.configure(bg="white")

    # === Encabezado ===
    header = tk.Frame(ventana, bg="#2e8b57", height=60)
    header.pack(fill="x")

    tk.Label(header, text=f"{empresa.upper()}", bg="#2e8b57", fg="white",
             font=("Arial", 14, "bold")).pack(side="left", padx=20)

    tk.Label(header, text=f"{nombre_usuario}\nOperador", bg="#2e8b57", fg="white",
             font=("Arial", 10), justify="right").pack(side="right", padx=20)

    # === Cuerpo ===
    cuerpo = tk.Frame(ventana, bg="white")
    cuerpo.pack(expand=True)

    tk.Label(cuerpo, text="¿Qué desea hacer?", font=("Arial", 12), bg="white").pack(pady=(40, 20))

    botones = [
        ("Cargar evento", cargar_evento),
        ("Modificar evento", modificar_evento),
        ("Eliminar evento", eliminar_evento)
    ]

    for texto, comando in botones:
        tk.Button(cuerpo, text=texto, width=25, font=("Arial", 11),
                  command=comando, bg="#2e8b57", fg="white").pack(pady=10)

    tk.Button(cuerpo, text="Salir", width=15, font=("Arial", 10),
              command=salir, bg="#888888", fg="white").pack(pady=30)

    ventana.mainloop()

