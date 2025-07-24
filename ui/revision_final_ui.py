# ui/revision_final_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from utils.eventos_storage import cargar_eventos, limpiar_eventos
from utils.excel_storage import export_revision, load_codes
import datetime


def centrar_ventana(ventana, ancho=800, alto=600):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.resizable(False, False)


def revision_final_operario(nombre_usuario, empresa, volver_func):
    eventos_data = cargar_eventos()

    try:
        codes_df = load_codes(empresa)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar códigos de la empresa: {e}")
        return

    rename_map = {}
    if "Codigo" in codes_df.columns:
        rename_map["Codigo"] = "station_number"
    if "Tipo de trampa" in codes_df.columns:
        rename_map["Tipo de trampa"] = "trap_type"
    if rename_map:
        codes_df = codes_df.rename(columns=rename_map)

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

    for mod in eventos_data:
        num_mod = str(mod.get("numero", ""))
        for evt in eventos_export:
            if evt["numero"] == num_mod:
                if mod.get("tipo_evento"):
                    evt["tipo_evento"] = mod["tipo_evento"]
                elif mod.get("evento"):
                    evt["tipo_evento"] = mod["evento"]
                if mod.get("observacion"):
                    evt["observacion"] = mod["observacion"]
                break

    eventos_modificados = [
        (evt["numero"], evt["tipo_estacion"], evt["tipo_evento"], evt["observacion"])
        for evt in eventos_export
        if evt["tipo_evento"] != "Normal" or evt["observacion"] != "Sin modificaciones"
    ]

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
        try:
            path = export_revision(empresa, eventos_export)
            messagebox.showinfo("Exportado", f"Archivo guardado en:\n{path}")
        except Exception as e:
            messagebox.showerror("Error al exportar", str(e))
            return
        limpiar_eventos()
        ventana.destroy()
        volver_func()

    def volver():
        ventana.destroy()
        volver_func()

    # === Ventana principal ===
    ventana = tk.Tk()
    ventana.title("Revisión Final de Eventos")
    centrar_ventana(ventana)
    ventana.configure(bg="white")

    # === Encabezado ===
    header = tk.Frame(ventana, bg="#2e8b57", height=60)
    header.pack(fill="x")

    tk.Label(header, text=f"{empresa.upper()} - {datetime.date.today().strftime('%d/%m/%Y')}",
             bg="#2e8b57", fg="white", font=("Arial", 13, "bold")).pack(side="left", padx=20)

    tk.Label(header, text=f"{nombre_usuario}\nOperador", bg="#2e8b57", fg="white",
             font=("Arial", 10), justify="right").pack(side="right", padx=20)

    # === Tabla ===
    cuerpo = tk.Frame(ventana, bg="white")
    cuerpo.pack(pady=20)

    tree = ttk.Treeview(cuerpo, columns=("numero", "tipo_estacion", "tipo_evento", "observacion"),
                        show="headings", height=12)
    for col, ancho in zip(["numero", "tipo_estacion", "tipo_evento", "observacion"],
                           [100, 180, 180, 300]):
        tree.heading(col, text=col.replace("_", " ").capitalize())
        tree.column(col, width=ancho)

    for fila in eventos_modificados:
        tree.insert("", "end", values=fila)

    tree.bind("<Double-1>", modificar_celda)
    tree.pack()

    # === Botones ===
    btn_frame = tk.Frame(ventana, bg="white")
    btn_frame.pack(pady=25)

    tk.Button(btn_frame, text="Atrás", width=15, command=volver,
              bg="#888888", fg="white", font=("Arial", 10)).grid(row=0, column=0, padx=15)

    tk.Button(btn_frame, text="Finalizar", width=15, command=finalizar_revision,
              bg="#2e8b57", fg="white", font=("Arial", 10)).grid(row=0, column=1, padx=15)

    ventana.mainloop()
