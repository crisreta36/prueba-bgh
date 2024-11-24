import cv2
import numpy as np
import tkinter as tk
from tkinter import Button
from threading import Thread
import json  # Para leer el archivo JSON
from database import registrar  # Si tienes la base de datos integrada

# Variable global para controlar cuándo detener la cámara
detener_camara = False

# Cargar el archivo JSON generado por Labelme
with open('imagenes/cable_placa.json') as archivo_json:
    datos_json = json.load(archivo_json)

# Rango de colores en HSV para los cables (modificar estos valores según los cables que tienes)
amarillo_bajo = np.array([20, 100, 100])
amarillo_alto = np.array([30, 255, 255])

rojo_bajo = np.array([0, 100, 100])
rojo_alto = np.array([10, 255, 255])

azul_bajo = np.array([100, 150, 0])
azul_alto = np.array([140, 255, 255])

verde_bajo = np.array([40, 50, 50])
verde_alto = np.array([80, 255, 255])

negro_bajo = np.array([0, 0, 0])
negro_alto = np.array([180, 255, 50])

# Función para detectar colores en un rango HSV
def detectar_color(frame, color_bajo, color_alto):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_bajo, color_alto)
    return mask

# Calcular el centro de un polígono (sacado del JSON)
def calcular_centro(puntos):
    puntos_np = np.array(puntos, np.int32)
    centro_x = np.mean(puntos_np[:, 0])
    centro_y = np.mean(puntos_np[:, 1])
    return int(centro_x), int(centro_y)

# Verificar la correcta ubicación de los cables comparando con las posiciones del JSON
def verificar_ubicacion(mask, nombre_color, frame, datos_json):
    contornos, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contorno in contornos:
        if cv2.contourArea(contorno) > 300:  # Ajusta este valor si es necesario
            (x, y, w, h) = cv2.boundingRect(contorno)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            
            # Verificar si el cable está en la posición correcta según el JSON
            for shape in datos_json['shapes']:
                if shape['label'] == nombre_color:
                    centro_json = calcular_centro(shape['points'])  # Calcular el centro del cable en el JSON
                    cv2.circle(frame, centro_json, 5, (0, 255, 0), -1)  # Dibujar el centro esperado en la imagen
                    
                    # Comparar la posición del cable detectado con el centro del JSON
                    if abs(centro_json[0] - x) < 20 and abs(centro_json[1] - y) < 20:  # Rango de tolerancia
                        cv2.putText(frame, f"{nombre_color} OK", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        return True
                    else:
                        cv2.putText(frame, f"{nombre_color} ERROR", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                        return False
    return False

# Iniciar la cámara para detección en tiempo real
def iniciar_camara():
    global detener_camara
    detener_camara = False  # Reiniciamos la variable al iniciar la cámara

    # Crear una ventana de Tkinter para colocar el botón "Detener Cámara"
    cam_window = tk.Toplevel()
    cam_window.title("Deteccion de Cables - BGH PowerCheck")
    cam_window.geometry("400x200")

    # Función para detener la cámara desde el botón
    def detener_desde_boton():
        global detener_camara
        detener_camara = True
        cam_window.destroy()

    # Agregamos un botón "Detener Cámara" dentro de la ventana de Tkinter
    btn_detener = Button(cam_window, text="Detener Cámara", font=("Arial", 16), command=detener_desde_boton)
    btn_detener.pack(pady=40)

    # Usamos un hilo para procesar el video sin bloquear la interfaz gráfica
    def procesar_video():
        global detener_camara
        cap = cv2.VideoCapture(0)  # Abre la cámara

        while True:
            ret, frame = cap.read()  # Captura frame por frame
            if not ret or detener_camara:  # Verifica si detener_camara se activó
                break

            # Detectar colores
            amarillo_mask = detectar_color(frame, amarillo_bajo, amarillo_alto)
            rojo_mask = detectar_color(frame, rojo_bajo, rojo_alto)
            azul_mask = detectar_color(frame, azul_bajo, azul_alto)
            verde_mask = detectar_color(frame, verde_bajo, verde_alto)
            negro_mask = detectar_color(frame, negro_bajo, negro_alto)

            # Verificar ubicaciones con base en el JSON
            amarillo_ok = verificar_ubicacion(amarillo_mask, 'caja_placa_cable_amarillo', frame, datos_json)
            rojo_ok = verificar_ubicacion(rojo_mask, 'caja_placa_blanca_cable_rojo_claro', frame, datos_json)
            azul_ok = verificar_ubicacion(azul_mask, 'caja_placa_blanca_cable_azul', frame, datos_json)
            verde_ok = verificar_ubicacion(verde_mask, 'caja_placa_blanca_cable_verde_amarillo', frame, datos_json)
            negro_ok = verificar_ubicacion(negro_mask, 'caja_placa_blanca_cable_negro', frame, datos_json)

            # Si todos los cables están OK, mostrar un mensaje en el frame
            if amarillo_ok and rojo_ok and azul_ok and verde_ok and negro_ok:
                cv2.putText(frame, "CONEXION CORRECTA", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "ERROR EN LA CONEXION", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # Mostrar el video en tiempo real con las detecciones
            cv2.imshow('BGH PowerCheck - Deteccion de Cables', frame)

            # Comprobar si se presiona la tecla 'q' para salir manualmente
            if cv2.waitKey(1) & 0xFF == ord('q'):
                detener_camara = True
                break

        cap.release()
        cv2.destroyAllWindows()

        # Registrar el evento como correcto o fallido según la detección (si tienes la función registrar)
        registrar("correcto")

    # Crear un hilo para la función procesar_video
    video_thread = Thread(target=procesar_video)
    video_thread.start()

    cam_window.mainloop()  # Iniciar el bucle de eventos de Tkinter
