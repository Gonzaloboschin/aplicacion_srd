import tkinter as tk
from tkinter import ttk, messagebox
from utils.eventos_storage import guardar_evento
from ui.revision_final_ui import revision_final_operario
from utils.codigo_estaciones import obtener_tipo_estacion_por_codigo



def abrir_cargar_evento(nombre_usuario, empresa, volver_func):

    def cargar():
        estacion = entry_estacion.get().strip()
        tipo_estacion = combo_tipo_estacion.get().strip()
        tipo_evento = combo_tipo_evento.get().strip()
        observacion = entry_observacion.get().strip()

        if not estacion or not tipo_estacion or not tipo_evento or not observacion:
            messagebox.showwarning("Campos incompletos", "Por favor complete todos los campos.")
            return

        # Guardar evento en archivo JSON
        guardar_evento(estacion, tipo_estacion, tipo_evento, observacion)

        messagebox.showinfo("Evento cargado", f"Estación: {estacion}\nTipo estación: {tipo_estacion}\nTipo evento: {tipo_evento}\nObs: {observacion}")

        entry_estacion.delete(0, tk.END)
        combo_tipo_estacion.set("")
        combo_tipo_evento.set("")
        entry_observacion.delete(0, tk.END)

    def volver_atras():
        ventana.destroy()
        volver_func()

    def finalizar():
        estacion = entry_estacion.get().strip()
        tipo_estacion = combo_tipo_estacion.get().strip()
        tipo_evento = combo_tipo_evento.get().strip()
        observacion = entry_observacion.get().strip()

        if estacion or tipo_estacion or tipo_evento or observacion:
            if not (estacion and tipo_estacion and tipo_evento and observacion):
                messagebox.showwarning("Campos incompletos", "Antes de finalizar, complete todos los campos o vacíelos.")
                return

            guardar_evento(estacion, tipo_estacion + ' - ' + tipo_evento, observacion)
            messagebox.showinfo("Evento guardado", "Tu evento fue guardado automáticamente antes de finalizar.")

        ventana.destroy()
        revision_final_operario(nombre_usuario, empresa, volver_func)
        
    def mostrar_info(texto):
        info_label.config(text=texto)

    def limpiar_info(_event=None):
        info_label.config(text="")


    def actualizar_tipo_estacion(_event=None):
        codigo = entry_estacion.get().strip()
        if not codigo.isdigit():
            return

        tipo = obtener_tipo_estacion_por_codigo(empresa, int(codigo))
        if tipo:
            combo_tipo_estacion.set(tipo)
            if tipo == "Cebadero Químico":
                combo_tipo_evento['values'] = ["Mojado", "Picado", "Comido", "Faltante"]
            elif tipo == "Planchas Pegamentosas":
                combo_tipo_evento['values'] = ["Mojada", "Vencida", "Faltante", "Con captura"]
            elif tipo == "Trampa Jaulas":
                combo_tipo_evento['values'] = ["Captura", "No captura", "Reactivada"]


    ventana = tk.Tk()
    ventana.title("Cargar evento")
    ventana.geometry("600x450")
    ventana.configure(bg="#FFCC00")

    # === Usuario arriba a la derecha ===
    label_usuario = tk.Label(ventana, text=f"{nombre_usuario}\nOperador", bg="#FFCC00", font=("Arial", 10), justify="right")
    label_usuario.place(relx=0.98, rely=0.02, anchor="ne")

    # === Frame central ===
    frame = tk.Frame(ventana, bg="#FFCC00")
    frame.place(relx=0.5, rely=0.45, anchor="center")

    label_titulo = tk.Label(frame, text="Registro de control", font=("Arial", 12, "bold"), bg="#FFCC00")
    label_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    # === Campos de entrada ===
    tk.Label(frame, text="Número de estación", bg="#FFCC00", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
    entry_estacion = tk.Entry(frame, font=("Arial", 10))
    entry_estacion.bind("<FocusOut>", actualizar_tipo_estacion)
    entry_estacion.grid(row=1, column=1, padx=5, pady=5)

    # Nuevo: Tipo de estación
    tk.Label(frame, text="Tipo de estación", bg="#FFCC00", font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
    combo_tipo_estacion = ttk.Combobox(frame, values=["Trampa Jaulas", "Planchas Pegamentosas", "Cebadero Químico"], state="readonly", font=("Arial", 10))
    combo_tipo_estacion.grid(row=2, column=1, padx=5, pady=5)

    # Tipo de evento dinámico o fijo según lógica futura
    tk.Label(frame, text="Tipo de evento", bg="#FFCC00", font=("Arial", 10)).grid(row=3, column=0, sticky="e", padx=5, pady=5)
    combo_tipo_evento = ttk.Combobox(frame, values=["Mojado", "Picado", "Faltante", "Vencida", "Faltante", "Con captura", "Sin captura"], state="readonly", font=("Arial", 10))
    combo_tipo_evento.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(frame, text="Observación", bg="#FFCC00", font=("Arial", 10)).grid(row=4, column=0, sticky="e", padx=5, pady=5)
    entry_observacion = tk.Entry(frame, font=("Arial", 10))
    entry_observacion.grid(row=4, column=1, padx=5, pady=5)

    # === Botones con eventos de hover ===
    botones_frame = tk.Frame(frame, bg="#FFCC00")
    botones_frame.grid(row=5, column=0, columnspan=2, pady=20)

    btn_atras = tk.Button(botones_frame, text="Atrás", width=10, command=volver_atras)
    btn_atras.grid(row=0, column=0, padx=10)

    btn_cargar = tk.Button(botones_frame, text="Cargar", width=10, command=cargar)
    btn_cargar.grid(row=0, column=1, padx=10)

    btn_finalizar = tk.Button(botones_frame, text="Finalizar", width=10, command=finalizar)
    btn_finalizar.grid(row=0, column=2, padx=10)

    # === Label informativo inferior ===
    info_label = tk.Label(ventana, text="", bg="#FFCC00", font=("Arial", 9), wraplength=500, justify="center")
    info_label.place(relx=0.5, rely=0.92, anchor="center")

    for btn, txt in [(btn_cargar, "Cuando se presiona 'Cargar', se agrega la modificación..."),
                     (btn_finalizar, "Si no hay más eventos que cargar..."),
                     (btn_atras, "Volver a la pantalla anterior sin guardar...")]:
        btn.bind("<Enter>", lambda e, t=txt: mostrar_info(t))
        btn.bind("<Leave>", limpiar_info)

    ventana.mainloop()
