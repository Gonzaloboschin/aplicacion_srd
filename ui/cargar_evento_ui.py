import tkinter as tk
from tkinter import ttk, messagebox

def abrir_cargar_evento(nombre_usuario, empresa):
    def cargar():
        estacion = entry_estacion.get()
        tipo = combo_tipo_evento.get()
        observacion = entry_observacion.get()

        if not estacion or not tipo or not observacion:
            messagebox.showwarning("Campos incompletos", "Por favor complete todos los campos.")
            return

        # Simulación de inserción en base de datos
        print(f"Evento cargado: Estación={estacion}, Tipo={tipo}, Obs={observacion}")

        entry_estacion.delete(0, tk.END)
        combo_tipo_evento.set("")
        entry_observacion.delete(0, tk.END)

    def finalizar():
        ventana.destroy()

    def volver_atras():
        ventana.destroy()

    def mostrar_info(texto):
        info_label.config(text=texto)

    def limpiar_info(_event=None):
        info_label.config(text="")

    ventana = tk.Tk()
    ventana.title("Cargar evento")
    ventana.geometry("600x400")
    ventana.configure(bg="#FFCC00")

    # === Usuario arriba a la derecha ===
    label_usuario = tk.Label(ventana, text=f"{nombre_usuario}\nOperador", bg="#FFCC00", font=("Arial", 10), justify="right")
    label_usuario.place(relx=0.98, rely=0.02, anchor="ne")

    # === Frame central ===
    frame = tk.Frame(ventana, bg="#FFCC00")
    frame.place(relx=0.5, rely=0.4, anchor="center")

    label_titulo = tk.Label(frame, text="Cargar evento", font=("Arial", 12, "bold"), bg="#FFCC00")
    label_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # === Campos de entrada ===
    tk.Label(frame, text="Número de estación", bg="#FFCC00", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_estacion = tk.Entry(frame, font=("Arial", 10))
    entry_estacion.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Tipo de evento", bg="#FFCC00", font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    combo_tipo_evento = ttk.Combobox(frame, values=["Seco", "Húmedo", "Mojado"], state="readonly", font=("Arial", 10))
    combo_tipo_evento.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame, text="Observación", bg="#FFCC00", font=("Arial", 10)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
    entry_observacion = tk.Entry(frame, font=("Arial", 10))
    entry_observacion.grid(row=3, column=1, padx=5, pady=5)

    # === Botones con eventos de hover ===
    # === Botones alineados horizontalmente ===
    botones_frame = tk.Frame(frame, bg="#FFCC00")
    botones_frame.grid(row=4, column=0, columnspan=2, pady=20)

    btn_atras = tk.Button(botones_frame, text="Atrás", width=10, command=volver_atras)
    btn_atras.grid(row=0, column=0, padx=10)

    btn_cargar = tk.Button(botones_frame, text="Cargar", width=10, command=cargar)
    btn_cargar.grid(row=0, column=1, padx=10)

    btn_finalizar = tk.Button(botones_frame, text="Finalizar", width=10, command=finalizar)
    btn_finalizar.grid(row=0, column=2, padx=10)


    # === Label informativo inferior ===
    info_label = tk.Label(ventana, text="", bg="#FFCC00", font=("Arial", 9), wraplength=500, justify="center")
    info_label.place(relx=0.5, rely=0.9, anchor="center")

    # === Asociar eventos hover a cada botón ===
    btn_cargar.bind("<Enter>", lambda e: mostrar_info(
        "Cuando se presiona 'Cargar', se agrega la modificación a la base de datos. "
        "Los campos se limpian para agregar otro evento."
    ))
    btn_cargar.bind("<Leave>", limpiar_info)

    btn_finalizar.bind("<Enter>", lambda e: mostrar_info(
        "Si no hay más eventos que cargar, presione 'Finalizar' para volver a la pantalla anterior."
    ))
    btn_finalizar.bind("<Leave>", limpiar_info)

    btn_atras.bind("<Enter>", lambda e: mostrar_info("Volver a la pantalla anterior sin guardar cambios."))
    btn_atras.bind("<Leave>", limpiar_info)

    ventana.mainloop()
