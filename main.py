import tkinter as tk
from tkinter import messagebox
from database import crear_bd, mostrar_fallidos, mostrar_correctos  # Importar funciones de database.py
from camera import iniciar_camara  # Ya no necesitas detener_camara_func

# Función para validar el login
def validate_login():
    username = entry_user.get()
    password = entry_pass.get()

    # Validación de usuario y contraseña (estático por ahora)
    if username == "admin" and password == "12345":
        messagebox.showinfo("Login Correcto", "Bienvenido a BGH PowerCheck")
        root.destroy()  # Cerramos la ventana de login
        mostrar_menu()
    else:
        messagebox.showerror("Error", "Credenciales Incorrectas")

# Función para el menú principal
def mostrar_menu():
    menu = tk.Tk()
    menu.title("BGH PowerCheck - Menú Principal")
    menu.geometry("600x400")  # Tamaño de la ventana del menú (ancho x alto) ok

    # Botón para iniciar la cámara
    btn_iniciar_cam = tk.Button(menu, text="Iniciar Cámara", font=("Arial", 14), command=iniciar_camara)
    btn_iniciar_cam.pack(pady=10)

    # Botón para ver registros fallidos
    btn_fallidos = tk.Button(menu, text="Registros Fallidos", font=("Arial", 14), command=mostrar_fallidos)
    btn_fallidos.pack(pady=10)

    # Botón para ver detecciones correctas
    btn_correctos = tk.Button(menu, text="Detecciones Correctas", font=("Arial", 14), command=mostrar_correctos)
    btn_correctos.pack(pady=10)

    # Botón para cerrar sesión y salir
    btn_cerrar_sesion = tk.Button(menu, text="Cerrar Sesión y Salir", font=("Arial", 14), command=lambda: cerrar_sesion(menu))
    btn_cerrar_sesion.pack(pady=20)

    menu.mainloop()

# Función para cerrar sesión y salir del sistema
def cerrar_sesion(menu):
    menu.destroy()  # Cierra el menú principal
    root.quit()  # Cierra todo el sistema

# Crear la ventana de inicio de sesión
root = tk.Tk()
root.title("BGH PowerCheck - Login")
root.geometry("400x300")  # Tamaño de la ventana de login (ancho x alto)

# Etiquetas y campos de texto
label_user = tk.Label(root, text="Usuario", font=("Arial", 14))
label_user.pack(pady=10)
entry_user = tk.Entry(root, font=("Arial", 14), width=20)
entry_user.pack(pady=10)

label_pass = tk.Label(root, text="Contraseña", font=("Arial", 14))
label_pass.pack(pady=10)
entry_pass = tk.Entry(root, show="*", font=("Arial", 14), width=20)
entry_pass.pack(pady=10)

# Botón de inicio de sesión
btn_login = tk.Button(root, text="Iniciar Sesión", font=("Arial", 14), command=validate_login)
btn_login.pack(pady=20)

# Iniciar la base de datos
crear_bd()  # Llamamos a la función para crear la base de datos si no existe

root.mainloop()
