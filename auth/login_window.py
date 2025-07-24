# auth/login_window.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

USERS_FILE = "users.json"
REMEMBER_FILE = "remember.json"
LOGO_PATH = "assets/logo_srd.png"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def load_remembered_user():
    if os.path.exists(REMEMBER_FILE):
        with open(REMEMBER_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("username", "")
    return ""


def save_remembered_user(username):
    with open(REMEMBER_FILE, "w", encoding="utf-8") as f:
        json.dump({"username": username}, f)


def centrar_ventana(ventana, ancho=400, alto=420):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    ventana.resizable(False, False)


def show_register():
    reg_win = tk.Toplevel()
    reg_win.title("Registrar Usuario")
    centrar_ventana(reg_win, 350, 350)
    reg_win.grab_set()

    frame = tk.Frame(reg_win, bg="white", padx=20, pady=20)
    frame.pack(expand=True)

    tk.Label(frame, text="Nuevo Usuario", bg="white").grid(row=0, column=0, sticky="w", pady=5)
    entry_user = tk.Entry(frame)
    entry_user.grid(row=0, column=1)

    tk.Label(frame, text="Contraseña", bg="white").grid(row=1, column=0, sticky="w", pady=5)
    entry_pass = tk.Entry(frame, show="*")
    entry_pass.grid(row=1, column=1)

    tk.Label(frame, text="Confirmar Contraseña", bg="white").grid(row=2, column=0, sticky="w", pady=5)
    entry_confirm = tk.Entry(frame, show="*")
    entry_confirm.grid(row=2, column=1)

    tk.Label(frame, text="Rol", bg="white").grid(row=3, column=0, sticky="w", pady=5)
    combo_roles = tk.StringVar(value="user")
    tk.OptionMenu(frame, combo_roles, "user", "admin").grid(row=3, column=1)

    def register_user():
        username = entry_user.get().strip()
        password = entry_pass.get()
        confirm = entry_confirm.get()
        role = combo_roles.get()

        if not username or not password:
            messagebox.showwarning("Atención", "Usuario y contraseña son obligatorios.", parent=reg_win)
            return

        users = load_users()
        if any(u.lower() == username.lower() for u in users):
            messagebox.showerror("Error", "El usuario ya existe.", parent=reg_win)
            return

        if password != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden.", parent=reg_win)
            return

        users[username] = {"password": password, "role": role}
        save_users(users)
        messagebox.showinfo("Éxito", f"Usuario '{username}' registrado.", parent=reg_win)
        reg_win.destroy()

    tk.Button(frame, text="Crear cuenta", bg="#2e8b57", fg="white", command=register_user).grid(row=4, column=0, columnspan=2, pady=20)


def show_login():
    result = {"username": None, "role": None}

    def toggle_password():
        if show_pass.get():
            entry_pass.config(show="")
        else:
            entry_pass.config(show="*")

    def validate_login():
        input_user = entry_user.get().strip()
        input_pass = entry_pass.get()

        users = load_users()
        matched_user = next((u for u in users if u.lower() == input_user.lower()), None)

        if matched_user and users[matched_user]["password"] == input_pass:
            result["username"] = matched_user
            result["role"] = users[matched_user]["role"]
            if remember_var.get():
                save_remembered_user(matched_user)
            else:
                save_remembered_user("")
            login_win.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos", parent=login_win)

    login_win = tk.Tk()
    login_win.title("San Rafael Desinfecciones")
    centrar_ventana(login_win)
    login_win.configure(bg="white")

    # === LOGO ===
    try:
        logo_img = Image.open(LOGO_PATH).resize((100, 100))
        logo = ImageTk.PhotoImage(logo_img)
        tk.Label(login_win, image=logo, bg="white").pack(pady=(10, 0))
    except Exception as e:
        print(f"[ERROR] No se pudo cargar logo: {e}")

    tk.Label(login_win, text="Bienvenido", bg="white", fg="#2e8b57", font=("Arial", 16, "bold")).pack(pady=(10, 5))

    form_frame = tk.Frame(login_win, bg="white")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Usuario", bg="white").grid(row=0, column=0, sticky="w", pady=5)
    entry_user = tk.Entry(form_frame, width=30)
    entry_user.grid(row=0, column=1, pady=5)
    entry_user.insert(0, load_remembered_user())

    tk.Label(form_frame, text="Contraseña", bg="white").grid(row=1, column=0, sticky="w", pady=5)
    entry_pass = tk.Entry(form_frame, show="*", width=30)
    entry_pass.grid(row=1, column=1, pady=5)

    show_pass = tk.BooleanVar(value=False)
    tk.Checkbutton(form_frame, text="Mostrar contraseña", variable=show_pass, bg="white", command=toggle_password).grid(row=2, column=1, sticky="w", pady=5)

    remember_var = tk.BooleanVar(value=bool(load_remembered_user()))
    tk.Checkbutton(form_frame, text="Recordarme", variable=remember_var, bg="white").grid(row=3, column=1, sticky="w", pady=5)

    btn_frame = tk.Frame(login_win, bg="white")
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Iniciar sesión", width=15, bg="#2e8b57", fg="white", command=validate_login).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Registrarse", width=15, bg="#888888", fg="white", command=show_register).grid(row=0, column=1, padx=10)

    login_win.mainloop()
    return result
