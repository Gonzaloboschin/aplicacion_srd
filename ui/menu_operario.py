# ui/revision_final_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from ui.cargar_evento_ui import abrir_cargar_evento


def menu_operario(nombre_usuario, empresa, volver_func):


    def cargar_evento():
        ventana.destroy()
        abrir_cargar_evento(nombre_usuario, empresa, lambda: menu_operario(nombre_usuario, empresa, volver_func))

    def modificar_evento():
        messagebox.showinfo("Modificar evento", "Abrir pantalla de modificación de evento")

    def eliminar_evento():
        messagebox.showinfo("Eliminar evento", "Abrir pantalla de eliminación de evento")

    def salir():
        messagebox.showinfo("Sesión finalizada", "La revisión fue completada. Volviendo al inicio.")
        ventana.destroy()
        volver_func()

    ventana = tk.Tk()
    ventana.title("Revisión final de eventos modificados")
    ventana.geometry("500x400")
    ventana.configure(bg="#FFCC00")

    label_usuario = tk.Label(ventana, text=f"{nombre_usuario}\nOperador", bg="#FFCC00", font=("Arial", 10), anchor="e", justify="right")
    label_usuario.place(relx=0.98, rely=0.02, anchor="ne")

    label_empresa = tk.Label(ventana, text=empresa.upper(), font=("Arial", 12, "bold"), bg="#FFCC00")
    label_empresa.place(relx=0.1, rely=0.25, anchor="w")

    btn_cargar = tk.Button(ventana, text="Cargar evento", width=25, command=cargar_evento)
    btn_cargar.place(relx=0.5, rely=0.4, anchor="center")

    btn_modificar = tk.Button(ventana, text="Modificar evento", width=25, command=modificar_evento)
    btn_modificar.place(relx=0.5, rely=0.5, anchor="center")

    btn_eliminar = tk.Button(ventana, text="Eliminar evento", width=25, command=eliminar_evento)
    btn_eliminar.place(relx=0.5, rely=0.6, anchor="center")

    # Frame y botón salir
    frame_botones = tk.Frame(ventana, bg="#FFCC00")
    frame_botones.place(relx=0.5, rely=0.75, anchor="center")

    btn_salir = tk.Button(frame_botones, text="Salir", width=15, command=salir)
    btn_salir.grid(row=0, column=0, padx=10)

    ventana.mainloop()
