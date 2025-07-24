# ui/operario_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from ui.menu_operario import menu_operario

EMPRESAS = ["Villa Atuel S.A", "La Española S.A", "Sunny S.A"]  # Esto luego se puede conectar a BBDD


def centrar_ventana(ventana, ancho=800, alto=600):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.resizable(False, False)


def abrir_interfaz_operario(nombre_usuario):
    def iniciar_revision():
        empresa = combo_empresas.get()
        if not empresa or empresa == "Seleccione empresa":
            messagebox.showwarning("Atención", "Debe seleccionar una empresa.")
            return

        messagebox.showinfo("Revisión iniciada", f"Se inició revisión para: {empresa}")
        ventana.destroy()
        menu_operario(nombre_usuario, empresa, lambda: abrir_interfaz_operario(nombre_usuario))

    ventana = tk.Tk()
    ventana.title("Panel de Operario")
    centrar_ventana(ventana)

    ventana.configure(bg="white")

    # === Encabezado ===
    header = tk.Frame(ventana, bg="#2e8b57", height=60)
    header.pack(fill="x")

    tk.Label(header, text="Panel de Operario", bg="#2e8b57", fg="white",
             font=("Arial", 16, "bold")).pack(side="left", padx=20)

    tk.Label(header, text=f"{nombre_usuario}\nOperador", bg="#2e8b57", fg="white",
             font=("Arial", 10), justify="right").pack(side="right", padx=20)

    # === Contenido central ===
    cuerpo = tk.Frame(ventana, bg="white")
    cuerpo.pack(expand=True)

    tk.Label(cuerpo, text="Seleccione la empresa:", bg="white",
             font=("Arial", 12)).pack(pady=(60, 10))

    combo_empresas = ttk.Combobox(cuerpo, values=EMPRESAS, state="readonly", font=("Arial", 12), width=30)
    combo_empresas.set("Seleccione empresa")
    combo_empresas.pack(pady=10)

    tk.Button(cuerpo, text="Iniciar revisión", command=iniciar_revision,
              font=("Arial", 12), bg="#2e8b57", fg="white", width=20).pack(pady=30)

    ventana.mainloop()
