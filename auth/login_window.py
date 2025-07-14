# auth/login_window.py

import tkinter as tk
from tkinter import messagebox
import json
import os

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def show_login():
    result = {"username": None, "role": None}

    def validate_login():
        username = entry_user.get()
        password = entry_pass.get()
        users = load_users()

        if username in users and users[username]["password"] == password:
            result["username"] = username
            result["role"] = users[username]["role"]
            login_win.destroy()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    login_win = tk.Tk()
    login_win.title("San Rafael Desinfecciones")
    login_win.geometry("350x200")

    tk.Label(login_win, text="Usuario").pack(pady=(10, 0))
    entry_user = tk.Entry(login_win)
    entry_user.pack()

    tk.Label(login_win, text="Contraseña").pack(pady=(10, 0))
    entry_pass = tk.Entry(login_win, show="*")
    entry_pass.pack()

    tk.Button(login_win, text="Iniciar sesión", command=validate_login).pack(pady=20)

    login_win.mainloop()

    return result
