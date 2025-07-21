import tkinter as tk
from tkinter import ttk, messagebox
import json
from utils.eventos_storage import cargar_eventos, limpiar_eventos


def revision_final_operario(nombre_usuario, empresa, volver_func):
    # Cargar eventos, cada evento debe incluir: numero, tipo_estacion, tipo_evento, observacion
    eventos_data = cargar_eventos()
    eventos_modificados = [
        (
            e.get("numero", ""),
            e.get("tipo_estacion", ""),
            e.get("tipo_evento", ""),
            e.get("observacion", "")
        )
        for e in eventos_data
    ]

    def modificar_celda(event):
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        fila_id = tree.identify_row(event.y)
        columna = tree.identify_column(event.x)
        col_index = int(columna.replace("#", "")) - 1
        x, y, width, height = tree.bbox(fila_id, columna)
        valor_actual = tree.set(fila_id, column=col_index)

        entry = tk.Entry(tree)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, valor_actual)
        entry.focus()

        def guardar_edicion(evt):
            tree.set(fila_id, column=col_index, value=entry.get())
            entry.destroy()

        entry.bind("<Return>", guardar_edicion)
        entry.bind("<FocusOut>", lambda e: entry.destroy())

    def finalizar_revision():
        messagebox.showinfo("Finalizado", "Revisión enviada a la base de datos intermedia.")
        limpiar_eventos()
        ventana.destroy()
        volver_func()

    def volver():
        ventana.destroy()
        volver_func()

    ventana = tk.Tk()
    ventana.title("Revisión final de eventos")
    ventana.geometry("800x400")
    ventana.configure(bg="#FFCC00")

    # Encabezado
    tk.Label(ventana, text=empresa.upper(), font=("Arial", 14, "bold"), bg="#FFCC00").place(x=30, y=20)
    tk.Label(ventana, text=f"{nombre_usuario}\nOperador", font=("Arial", 10), bg="#FFCC00", justify="right").place(x=750, y=20)

    import datetime
    fecha = datetime.date.today().strftime("%d/%m/%Y")
    tk.Label(ventana, text=fecha, font=("Arial", 10), bg="#FFCC00").place(x=30, y=50)

    # Tabla con cuatro columnas: estación, tipo_estacion, tipo_evento, observacion
    tree = ttk.Treeview(
        ventana,
        columns=("numero", "tipo_estacion", "tipo_evento", "observacion"),
        show="headings",
        height=8
    )
    tree.heading("numero", text="Número de estación")
    tree.heading("tipo_estacion", text="Tipo de estación")
    tree.heading("tipo_evento", text="Tipo de evento")
    tree.heading("observacion", text="Observación")
    tree.column("numero", width=120)
    tree.column("tipo_estacion", width=150)
    tree.column("tipo_evento", width=150)
    tree.column("observacion", width=280)
    tree.place(relx=0.5, rely=0.55, anchor="center")

    # Insertar filas directamente sin división de cadenas
    for fila in eventos_modificados:
        tree.insert("", "end", values=fila)

    tree.bind("<Double-1>", modificar_celda)

    # Botones
    btn_frame = tk.Frame(ventana, bg="#FFCC00")
    btn_frame.pack(side="bottom", pady=20)

    tk.Button(btn_frame, text="Atrás", width=15, command=volver).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Finalizar", width=15, command=finalizar_revision).grid(row=0, column=1, padx=10)

    ventana.mainloop()
