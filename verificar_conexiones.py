from ultralytics import YOLO
import cv2

# Cargar el modelo entrenado
model = YOLO("runs/detect/cable_detector157/weights/best.pt")

def verificar_conexiones(results):
    conexiones = {
        "negro": "desconocido",
        "azul": "desconocido",
        "marron": "desconocido",
        "amarillo": "desconocido",
        "rojo": "desconocido"
    }

    for result in results:
        for box in result.boxes:
            clase = int(box.cls[0])
            score = float(box.conf[0])

            if score > 0.5:  # Considerar detecciones con confianza mayor al 50%
                if clase == 0:
                    conexiones["negro"] = "ok"
                elif clase == 1:
                    conexiones["azul"] = "ok"
                elif clase == 2:
                    conexiones["marron"] = "ok"
                elif clase == 3:
                    conexiones["amarillo"] = "ok"
                elif clase == 4:
                    conexiones["rojo"] = "ok"
                elif clase == 5:
                    conexiones["negro"] = "mala_conexion"
                elif clase == 6:
                    conexiones["azul"] = "mala_conexion"
                elif clase == 7:
                    conexiones["marron"] = "mala_conexion"
                elif clase == 8:
                    conexiones["amarillo"] = "mala_conexion"
                elif clase == 9:
                    conexiones["rojo"] = "mala_conexion"

    return conexiones

# Captura de cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Realizar detección
    results = model(frame)
    conexiones = verificar_conexiones(results)

    # Mostrar estado de las conexiones
    print(conexiones)

    # Mostrar resultados en la cámara
    annotated_frame = results[0].plot()
    cv2.imshow("Detección", annotated_frame)

    # Presionar 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
