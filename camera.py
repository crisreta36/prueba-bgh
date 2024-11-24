import cv2
from ultralytics import YOLO

def main():
    # Cargar el modelo entrenado
    model_path = "scripts/runs/detect/cable_detector157/weights/best.pt"  # Ajusta la ruta si es necesario
    try:
        model = YOLO(model_path)
        print(f"Modelo cargado correctamente desde: {model_path}")
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        return

    # Inicializar la cámara
    cap = cv2.VideoCapture(0)  # Cambia el índice si tienes varias cámaras
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    print("Presiona 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar el frame de la cámara.")
            break

        # Realizar predicciones
        try:
            results = model.predict(frame, conf=0.3)  # Ajusta el umbral de confianza si es necesario
            annotated_frame = results[0].plot()  # Dibujar las detecciones en el frame
        except Exception as e:
            print(f"Error durante la predicción: {e}")
            annotated_frame = frame

        # Mostrar el frame con las detecciones
        cv2.imshow("Detección de cables", annotated_frame)

        # Salir si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
