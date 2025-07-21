# auth/login_window.py

import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def show_register():
    """Abre una ventana para registrar un nuevo usuario."""
    reg_win = tk.Toplevel()
    reg_win.title("Registrar Usuario")
    reg_win.geometry("300x250")
    reg_win.grab_set()  # modal

    tk.Label(reg_win, text="Nuevo Usuario").pack(pady=(10, 0))
    entry_user = tk.Entry(reg_win)
    entry_user.pack()

    tk.Label(reg_win, text="Contraseña").pack(pady=(10, 0))
    entry_pass = tk.Entry(reg_win, show="*")
    entry_pass.pack()

    tk.Label(reg_win, text="Confirmar Contraseña").pack(pady=(10, 0))
    entry_confirm = tk.Entry(reg_win, show="*")
    entry_confirm.pack()

    tk.Label(reg_win, text="Rol").pack(pady=(10, 0))
    combo_roles = tk.StringVar(value="user")
    opcion_rol = tk.OptionMenu(reg_win, combo_roles, "user", "admin")
    opcion_rol.pack()

    def register_user():
        username = entry_user.get().strip()
        password = entry_pass.get()
        confirm = entry_confirm.get()
        role = combo_roles.get()

        if not username or not password:
            messagebox.showwarning("Atención", "Usuario y contraseña son obligatorios.", parent=reg_win)
            return

        users = load_users()
        # Verificar duplicado de usuario (case-insensitive)
        for u in users:
            if u.lower() == username.lower():
                messagebox.showerror("Error", "El usuario ya existe.", parent=reg_win)
                return

        if password != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden.", parent=reg_win)
            return

        # Agregar nuevo usuario
        users[username] = {
            "password": password,
            "role": role
        }
        save_users(users)
        messagebox.showinfo("Éxito", f"Usuario '{username}' registrado.", parent=reg_win)
        reg_win.destroy()

    tk.Button(reg_win, text="Crear cuenta", command=register_user).pack(pady=15)

def show_login():
    result = {"username": None, "role": None}

    def validate_login():
        input_user = entry_user.get().strip()
        input_pass = entry_pass.get()

        users = load_users()
        # Buscamos un usuario cuyo nombre, en minúsculas, coincida con la entrada en minúsculas
        matched_user = None
        for stored_user in users:
            if stored_user.lower() == input_user.lower():
                matched_user = stored_user
                break

        if matched_user and users[matched_user]["password"] == input_pass:
            result["username"] = matched_user
            result["role"] = users[matched_user]["role"]
            login_win.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos", parent=login_win)

    login_win = tk.Tk()
    login_win.title("San Rafael Desinfecciones")
    login_win.geometry("350x220")

    tk.Label(login_win, text="Usuario").pack(pady=(10, 0))
    entry_user = tk.Entry(login_win)
    entry_user.pack()

    tk.Label(login_win, text="Contraseña").pack(pady=(10, 0))
    entry_pass = tk.Entry(login_win, show="*")
    entry_pass.pack()

    btn_frame = tk.Frame(login_win)
    btn_frame.pack(pady=15)

    tk.Button(btn_frame, text="Iniciar sesión", width=12, command=validate_login).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Registrarse", width=12, command=show_register).grid(row=0, column=1, padx=5)

    login_win.mainloop()
    return result
