import os

def check_label_image_match(image_folder, label_folder):
    # Obtener nombres base de imágenes y etiquetas
    images = {os.path.splitext(file)[0] for file in os.listdir(image_folder) if file.endswith(('.jpg', '.png'))}
    labels = {os.path.splitext(file)[0] for file in os.listdir(label_folder) if file.endswith('.txt')}
    
    # Encontrar desajustes
    images_without_labels = images - labels  # Imágenes sin etiquetas
    labels_without_images = labels - images  # Etiquetas sin imágenes

    return images_without_labels, labels_without_images

# Rutas
image_folder = "D:/CIENCIA-DE-DATOS-IA-4TO-CUATRIMESTRE/Practica-profecionalizantes-2/Sistema-BGH-Cable-Detection/BGH_PowerCheck/datasets/train/images/correct"
label_folder = "D:/CIENCIA-DE-DATOS-IA-4TO-CUATRIMESTRE/Practica-profecionalizantes-2/Sistema-BGH-Cable-Detection/BGH_PowerCheck/datasets/train/labels/correct"

# Verificar correspondencia
images_without_labels, labels_without_images = check_label_image_match(image_folder, label_folder)

# Mostrar resultados
print(f"Imágenes sin etiquetas: {len(images_without_labels)}")
print(f"Etiquetas sin imágenes: {len(labels_without_images)}")

if images_without_labels:
    print("Imágenes sin etiquetas:")
    for img in images_without_labels:
        print(img)

if labels_without_images:
    print("Etiquetas sin imágenes:")
    for lbl in labels_without_images:
        print(lbl)
