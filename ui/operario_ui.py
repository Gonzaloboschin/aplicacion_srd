# ui/operario_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from ui.revision_operario_ui import abrir_revision_operario

EMPRESAS = ["Villa Atuel S.A", "La Española S.A", "Sunny S.A"] # DESPUES USAR BBDD

def abrir_interfaz_operario(nombre_usuario):

    def iniciar_revision(ventana):
        empresa = combo_empresas.get()
        if not empresa:
            messagebox.showwarning("Atención", "Debe seleccionar una empresa.")
            return

        # Mensaje informativo
        messagebox.showinfo("Revisión iniciada", f"Se inició revisión para: {empresa}\nEstado: todas las trampas en NORMAL")

        # Cerramos la ventana actual (asegurate que esté definida global o accesible)
        ventana.destroy()

        # Abrimos la nueva interfaz
        abrir_revision_operario(nombre_usuario, empresa)


    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Panel de Operario")
    ventana.geometry("500x300")
    ventana.configure(bg="#FFCC00")  # Amarillo de fondo como en la imagen

    # Usuario arriba a la derecha
    label_usuario = tk.Label(ventana, text=f"{nombre_usuario}\nOperador", bg="#FFCC00", font=("Arial", 10), anchor="e", justify="right")
    label_usuario.place(relx=0.98, rely=0.02, anchor="ne")

    # ComboBox para seleccionar empresa
    combo_empresas = ttk.Combobox(ventana, values=EMPRESAS, state="readonly", font=("Arial", 12))
    combo_empresas.set("Seleccione empresa")
    combo_empresas.place(relx=0.5, rely=0.4, anchor="center", width=250)

    # Botón Iniciar revisión
    btn_revision = tk.Button(ventana, text="Iniciar revisión", command=lambda: iniciar_revision(ventana), font=("Arial", 12), width=20)
    btn_revision.place(relx=0.5, rely=0.55, anchor="center")

    ventana.mainloop()
