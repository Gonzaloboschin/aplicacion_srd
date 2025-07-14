# ui/revision_operario_ui.py

import tkinter as tk
from tkinter import messagebox
from ui.cargar_evento_ui import abrir_cargar_evento


def abrir_revision_operario(nombre_usuario, empresa):

    def cargar_evento():
        ventana.destroy()
        abrir_cargar_evento(nombre_usuario, lambda: abrir_revision_operario(nombre_usuario, empresa))


    def modificar_evento():
        messagebox.showinfo("Modificar evento", "Abrir pantalla de modificación de evento")

    def eliminar_evento():
        messagebox.showinfo("Eliminar evento", "Abrir pantalla de eliminación de evento")

    def siguiente():
        messagebox.showinfo("Siguiente", "Continuar flujo")

    ventana = tk.Tk()
    ventana.title("Revisión - Operario")
    ventana.geometry("500x400")
    ventana.configure(bg="#FFCC00")

    # Usuario arriba a la derecha
    label_usuario = tk.Label(ventana, text=f"{nombre_usuario}\nOperador", bg="#FFCC00", font=("Arial", 10), anchor="e", justify="right")
    label_usuario.place(relx=0.98, rely=0.02, anchor="ne")

    # Nombre de la empresa en negrita
    label_empresa = tk.Label(ventana, text=empresa.upper(), font=("Arial", 12, "bold"), bg="#FFCC00")
    label_empresa.place(relx=0.1, rely=0.25, anchor="w")

    # Botones verticales
    btn_cargar = tk.Button(ventana, text="Cargar evento", width=25, command=cargar_evento)
    btn_cargar.place(relx=0.5, rely=0.4, anchor="center")

    btn_modificar = tk.Button(ventana, text="Modificar evento", width=25, command=modificar_evento)
    btn_modificar.place(relx=0.5, rely=0.5, anchor="center")

    btn_eliminar = tk.Button(ventana, text="Eliminar evento", width=25, command=eliminar_evento)
    btn_eliminar.place(relx=0.5, rely=0.6, anchor="center")

    btn_siguiente = tk.Button(ventana, text="Siguiente", width=25, command=siguiente)
    btn_siguiente.place(relx=0.5, rely=0.7, anchor="center")

    ventana.mainloop()


