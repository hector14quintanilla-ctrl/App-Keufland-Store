import tkinter as tk
from email import message
from tkinter import ttk, messagebox
from customtkinter import *
import os

# Diccionario que guarda los usuarios
accounts = {
    "username": "hector salamanca",
    "password": "1234"
}


# Funciones

def start_main_application():
    import app
    root = tk.Tk()
    pos_app = app.POSSystem(root)
    root.mainloop()


def perform_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == '' or password == '':
        messagebox.showinfo("", "No puedes ingresar un datos vacíos")
    elif username == accounts["username"] and password == accounts["password"]:
        messagebox.showinfo("", "Iniciando Sesión... ")
        window.destroy()
        start_main_application()
    else:
        messagebox.showinfo(
            "", "Usuario o Contraseña Invalidos, Intente de nuevo")


def policies_sec():
    try:
        with open("politicas_seguridad.txt", "r", encoding="utf-8") as archivo_politicas:
            messagebox.showwarning("Política de Seguridad para el Acceso al Sistema",
                                   archivo_politicas.read())
    except Exception:
        messagebox.showwarning("Error", "Error al leer el archivo")

        # Configuración de Pantalla
window = CTk()
window.geometry("900x600")
window.title("Login UI")
window.configure(fg_color="white")


# Creación del Frame
frame = CTkFrame(window, fg_color="#999999")
# Rel es el valor relativo de x o y de la pantalla
frame.place(relx=0.37, rely=0.37)

# Parte de Usuarios
username_label = CTkLabel(
    frame, text="👤 Usuario del Empleado", font=("Math Sans Bold", 17))
username_label.grid(row=0, column=0, pady=(0, 3))

username_entry = CTkEntry(frame, width=200)
# Row = 1 para que este debajo del texto de "Usuario del Empleado"
username_entry.grid(row=1, column=0)

# Parte de PIN
password_label = CTkLabel(frame, text="PIN", font=(
    "Math Sans Bold", 17))
password_label.grid(row=2, column=0)

password_entry = CTkEntry(frame, width=100, show="*")
password_entry.grid(row=3, column=0)

# Bóton Login

login_button = CTkButton(frame, text=" INICIAR SESIÓN ",
                         font=("Math Sans Bold", 14), hover_color="red", command=perform_login)
login_button.grid(row=4, column=0, pady=(0, 5))

# Frames para botones adiccionales
buttons_ad_frame = CTkFrame(window, fg_color="transparent")
buttons_ad_frame.place(relx=0.5, rely=4, anchor="center")

# Boton POLITICAS DE SEGURIDAD
policies_sec_button = CTkButton(
    window, text="Politicas de Seguridad", fg_color="red", width=220, height=35, command=policies_sec)
policies_sec_button.place(x=680, y=560)

window.mainloop()  # Tiene que estar al final de todo para que cargue lo que esta atras de el
