# ui/cargar_evento_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from utils.eventos_storage import guardar_evento
from ui.revision_final_ui import revision_final_operario
from utils.codigo_estaciones import obtener_tipo_estacion_por_codigo


def centrar_ventana(ventana, ancho=800, alto=600):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.resizable(False, False)


def abrir_cargar_evento(nombre_usuario, empresa, volver_func):
    def cargar():
        estacion = entry_estacion.get().strip()
        tipo_estacion = combo_tipo_estacion.get().strip()
        tipo_evento = combo_tipo_evento.get().strip()
        observacion = entry_observacion.get().strip()

        if not estacion or not tipo_estacion or not tipo_evento or not observacion:
            messagebox.showwarning("Campos incompletos", "Por favor complete todos los campos.")
            return

        guardar_evento(estacion, tipo_estacion, tipo_evento, observacion)

        messagebox.showinfo("Evento cargado", f"Estación: {estacion}\nTipo estación: {tipo_estacion}\nTipo evento: {tipo_evento}\nObs: {observacion}")

        entry_estacion.delete(0, tk.END)
        combo_tipo_estacion.set("")
        combo_tipo_evento.set("")
        entry_observacion.delete(0, tk.END)

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

    def actualizar_tipo_estacion(_event=None):
        codigo = entry_estacion.get().strip()
        if not codigo.isdigit():
            return

        tipo = obtener_tipo_estacion_por_codigo(empresa, int(codigo))
        if not tipo:
            messagebox.showerror("Código inválido", f"El código {codigo} no está definido para la empresa {empresa}.")
            combo_tipo_estacion.set("")
            combo_tipo_evento.set("")
            return

        combo_tipo_estacion.set(tipo)

        if tipo == "Cebadero Químico":
            combo_tipo_evento['values'] = ["Mojado", "Picado", "Comido", "Faltante"]
        elif tipo == "Planchas Pegamentosas":
            combo_tipo_evento['values'] = ["Mojada", "Vencida", "Faltante", "Con captura"]
        elif tipo == "Trampa Jaulas":
            combo_tipo_evento['values'] = ["Captura", "No captura", "Reactivada"]

    def volver_atras():
        ventana.destroy()
        volver_func()

    ventana = tk.Tk()
    ventana.title("Cargar Evento")
    centrar_ventana(ventana)
    ventana.configure(bg="white")

    # === Encabezado ===
    header = tk.Frame(ventana, bg="#2e8b57", height=60)
    header.pack(fill="x")

    tk.Label(header, text=f"{empresa.upper()}", bg="#2e8b57", fg="white",
             font=("Arial", 14, "bold")).pack(side="left", padx=20)

    tk.Label(header, text=f"{nombre_usuario}\nOperador", bg="#2e8b57", fg="white",
             font=("Arial", 10), justify="right").pack(side="right", padx=20)

    # === Formulario ===
    cuerpo = tk.Frame(ventana, bg="white")
    cuerpo.pack(pady=40)

    campos = [
        ("Número de estación", tk.Entry, "entry_estacion"),
        ("Tipo de estación", ttk.Combobox, "combo_tipo_estacion"),
        ("Tipo de evento", ttk.Combobox, "combo_tipo_evento"),
        ("Observación", tk.Entry, "entry_observacion")
    ]

    for i, (label_txt, widget_cls, var_name) in enumerate(campos):
        tk.Label(cuerpo, text=label_txt, bg="white", font=("Arial", 11)).grid(row=i, column=0, sticky="e", pady=8, padx=10)

        widget = widget_cls(cuerpo, font=("Arial", 11), width=30)
        widget.grid(row=i, column=1, pady=8, padx=10)

        globals()[var_name] = widget

    combo_tipo_estacion['state'] = "readonly"
    combo_tipo_estacion['values'] = ["Trampa Jaulas", "Planchas Pegamentosas", "Cebadero Químico"]

    combo_tipo_evento['state'] = "readonly"

    entry_estacion.bind("<FocusOut>", actualizar_tipo_estacion)

    # === Botones ===
    btn_frame = tk.Frame(ventana, bg="white")
    btn_frame.pack(pady=30)

    botones = [
        ("Atrás", volver_atras, "#888888"),
        ("Cargar", cargar, "#2e8b57"),
        ("Finalizar", finalizar, "#2e8b57")
    ]

    for i, (texto, cmd, color) in enumerate(botones):
        tk.Button(btn_frame, text=texto, command=cmd,
                  font=("Arial", 10), width=12, bg=color, fg="white").grid(row=0, column=i, padx=15)

    ventana.mainloop()
