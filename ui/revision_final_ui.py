import tkinter as tk
from tkinter import ttk, messagebox
from utils.eventos_storage import cargar_eventos, limpiar_eventos
from utils.excel_storage import export_revision, load_codes


def revision_final_operario(nombre_usuario, empresa, volver_func):
    # 1. Cargar eventos modificados (temp storage)
    eventos_data = cargar_eventos()

    # 2. Cargar catálogo estático de códigos para la empresa
    try:
        codes_df = load_codes(empresa)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar códigos de la empresa: {e}")
        return

    # 2.1 Asegurar que los nombres de columna coincidan con los esperados
    rename_map = {}
    if "Codigo" in codes_df.columns:
        rename_map["Codigo"] = "station_number"
    if "Tipo de trampa" in codes_df.columns:
        rename_map["Tipo de trampa"] = "trap_type"
    if rename_map:
        codes_df = codes_df.rename(columns=rename_map)

    # 3. Preparar lista completa con valores por defecto
    eventos_export = []
    for _, row in codes_df.iterrows():
        numero = str(row.get("station_number", ""))
        tipo_estacion = row.get("trap_type", "")
        eventos_export.append({
            "numero": numero,
            "tipo_estacion": tipo_estacion,
            "tipo_evento": "Normal",
            "observacion": "Sin modificaciones"
        })

    # 4. Aplicar modificaciones reales
    for mod in eventos_data:
        num_mod = str(mod.get("numero", ""))
        for evt in eventos_export:
            if evt["numero"] == num_mod:
                # actualizar tipo_evento si existe
                if mod.get("tipo_evento"):
                    evt["tipo_evento"] = mod.get("tipo_evento")
                elif mod.get("evento"):
                    evt["tipo_evento"] = mod.get("evento")
                # actualizar observacion
                if mod.get("observacion"):
                    evt["observacion"] = mod.get("observacion")
                break

    # 5. Filtrar solo modificaciones para mostrar en la UI
    eventos_modificados = []
    for evt in eventos_export:
        if evt["tipo_evento"] != "Normal" or evt["observacion"] != "Sin modificaciones":
            eventos_modificados.append((evt["numero"], evt["tipo_estacion"], evt["tipo_evento"], evt["observacion"]))

    def modificar_celda(event):
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        row_id = tree.identify_row(event.y)
        col = tree.identify_column(event.x)
        col_index = int(col.replace("#", "")) - 1
        x, y, width, height = tree.bbox(row_id, col)
        valor = tree.set(row_id, column=col_index)

        entry = tk.Entry(tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, valor)
        entry.focus()

        def on_commit(evt_arg):
            tree.set(row_id, column=col_index, value=entry.get())
            entry.destroy()

        entry.bind("<Return>", on_commit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    def finalizar_revision():
        # Exportar todo el catálogo con modificaciones
        try:
            path = export_revision(empresa, eventos_export)
            messagebox.showinfo("Exportado", f"Archivo guardado en:\n{path}")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))
            return
        # Limpiar temporal y cerrar
        limpiar_eventos()
        ventana.destroy()
        volver_func()

    def volver():
        ventana.destroy()
        volver_func()

    # --- Construcción de la UI ---
    ventana = tk.Tk()
    ventana.title("Revisión final de eventos")
    ventana.geometry("800x450")
    ventana.configure(bg="#FFCC00")

    # Encabezado
    tk.Label(ventana, text=empresa.upper(), font=("Arial", 14, "bold"), bg="#FFCC00").place(x=30, y=20)
    tk.Label(ventana, text=f"{nombre_usuario}\nOperador", font=("Arial", 10), bg="#FFCC00", justify="right").place(x=750, y=20)

    import datetime
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    tk.Label(ventana, text=fecha, font=("Arial", 10), bg="#FFCC00").place(x=30, y=50)

    # Tabla con solo registros modificados
    tree = ttk.Treeview(ventana, columns=("numero", "tipo_estacion", "tipo_evento", "observacion"), show="headings", height=8)
    tree.heading("numero", text="Número de estación")
    tree.heading("tipo_estacion", text="Tipo de estación")
    tree.heading("tipo_evento", text="Tipo de evento")
    tree.heading("observacion", text="Observación")
    tree.column("numero", width=120)
    tree.column("tipo_estacion", width=150)
    tree.column("tipo_evento", width=150)
    tree.column("observacion", width=280)
    tree.place(relx=0.5, rely=0.58, anchor="center")

    for fila in eventos_modificados:
        tree.insert("", "end", values=fila)

    tree.bind("<Double-1>", modificar_celda)

    # Botones
    btn_frame = tk.Frame(ventana, bg="#FFCC00")
    btn_frame.pack(side="bottom", pady=20)
    tk.Button(btn_frame, text="Atrás", width=15, command=volver).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Finalizar", width=15, command=finalizar_revision).grid(row=0, column=1, padx=10)

    ventana.mainloop()
