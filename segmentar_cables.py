import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('imagenes/cable_placa.jpeg')


# Convertir a espacio de color HSV
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Definir los rangos de colores para cada cable en HSV
# Estos valores pueden necesitar ajustes dependiendo de la iluminación y color
amarillo_bajo = np.array([20, 100, 100])  
amarillo_alto = np.array([30, 255, 255])

rojo_bajo = np.array([0, 100, 100])
rojo_alto = np.array([10, 255, 255])

azul_bajo = np.array([100, 150, 0])
azul_alto = np.array([140, 255, 255])

verde_bajo = np.array([40, 50, 50])
verde_alto = np.array([80, 255, 255])

# Crear máscaras para los diferentes colores de cables
amarillo_mask = cv2.inRange(hsv, amarillo_bajo, amarillo_alto)
rojo_mask = cv2.inRange(hsv, rojo_bajo, rojo_alto)
azul_mask = cv2.inRange(hsv, azul_bajo, azul_alto)
verde_mask = cv2.inRange(hsv, verde_bajo, verde_alto)

# Encontrar contornos para cada color de cable
def encontrar_contornos(mask, color_nombre):
    contornos, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contorno in contornos:
        if cv2.contourArea(contorno) > 300:  # Solo considerar contornos grandes
            x, y, w, h = cv2.boundingRect(contorno)
            cv2.rectangle(imagen, (x, y), (x+w, y+h), (255, 255, 255), 2)
            cv2.putText(imagen, color_nombre, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

# Etiquetar y dibujar los contornos de cada cable
encontrar_contornos(amarillo_mask, 'Cable Amarillo')
encontrar_contornos(rojo_mask, 'Cable Rojo')
encontrar_contornos(azul_mask, 'Cable Azul')
encontrar_contornos(verde_mask, 'Cable Verde')

# Mostrar la imagen segmentada y etiquetada
cv2.imshow('Cables Etiquetados', imagen)

# Guardar la imagen segmentada
cv2.imwrite('imagen_segmentada_y_etiquetada.jpg', imagen)

cv2.waitKey(0)
cv2.destroyAllWindows()
