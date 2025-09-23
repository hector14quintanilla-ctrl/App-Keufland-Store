from tkinter import messagebox
from customtkinter import *
# Funciones


def perform_login():
    username = username_entry.get()
    password = password_entry.get()

    if username == '' or password == '':
        messagebox.showinfo("", "No puedes ingresar un datos vacíos")
    elif username == 'Admin' and password == "1234":
        messagebox.showinfo("", "Iniciando Sesión... ")
        window.destroy()

    else:
        messagebox.showinfo(
            "", "Usuario o Contraseña Invalidos, Intente de nuevo")


# Configuración de Pantalla
window = CTk()
window.geometry("800x600")
window.title("Login UI")
window.configure(fg_color="white")


# Creación del Frame
frame = CTkFrame(window, fg_color="#5b5b5b")
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
password_label = CTkLabel(frame, text="PIN", font=("Math Sans Bold", 17))
password_label.grid(row=2, column=0)

password_entry = CTkEntry(frame, width=100, show="*")
password_entry.grid(row=3, column=0)

# Bóton Login

login_button = CTkButton(frame, text=" INICIAR SESIÓN ",
                         font=("Math Sans Bold", 14), hover_color="red", command=perform_login)
login_button.grid(row=4, column=0, pady=(0, 5))

window.mainloop()  # Tiene que estar al final de todo para que cargue lo que esta atras de el
