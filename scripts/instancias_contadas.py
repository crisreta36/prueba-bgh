import os

# Función para contar archivos en una carpeta
def count_files(folder, extensions=None):
    if not os.path.exists(folder):
        print(f"Ruta no encontrada: {folder}")
        return 0
    count = 0
    for file in os.listdir(folder):
        if extensions:
            if file.endswith(extensions):
                count += 1
        else:
            count += 1
    return count

# Función para contar líneas (instancias) en los archivos .txt
def count_instances_in_labels(folder):
    if not os.path.exists(folder):
        print(f"Ruta no encontrada: {folder}")
        return 0
    instance_count = 0
    for file in os.listdir(folder):
        if file.endswith('.txt'):
            with open(os.path.join(folder, file), 'r') as f:
                instance_count += len(f.readlines())
    return instance_count

# Rutas
paths = {
    "train_labels_correct": "D:/CIENCIA-DE-DATOS-IA-4TO-CUATRIMESTRE/Practica-profecionalizantes-2/Sistema-BGH-Cable-Detection/BGH_PowerCheck/datasets/train/labels/correct",
    "train_labels_incorrect": "D:/CIENCIA-DE-DATOS-IA-4TO-CUATRIMESTRE/Practica-profecionalizantes-2/Sistema-BGH-Cable-Detection/BGH_PowerCheck/datasets/train/labels/incorrect",
    "val_labels_correct": "D:/CIENCIA-DE-DATOS-IA-4TO-CUATRIMESTRE/Practica-profecionalizantes-2/Sistema-BGH-Cable-Detection/BGH_PowerCheck/datasets/val/labels/correct",
    "val_labels_incorrect": "D:/CIENCIA-DE-DATOS-IA-4TO-CUATRIMESTRE/Practica-profecionalizantes-2/Sistema-BGH-Cable-Detection/BGH_PowerCheck/datasets/val/labels/incorrect",
    "train_images_correct": "D:/CIENCIA-DE-DATOS-IA-4TO-CUATRIMESTRE/Practica-profecionalizantes-2/Sistema-BGH-Cable-Detection/BGH_PowerCheck/datasets/train/images/correct",
    "train_images_incorrect": "D:/CIENCIA-DE-DATOS-IA-4TO-CUATRIMESTRE/Practica-profecionalizantes-2/Sistema-BGH-Cable-Detection/BGH_PowerCheck/datasets/train/images/incorrect",
    "val_images_correct": "D:/CIENCIA-DE-DATOS-IA-4TO-CUATRIMESTRE/Practica-profecionalizantes-2/Sistema-BGH-Cable-Detection/BGH_PowerCheck/datasets/val/images/correct",
    "val_images_incorrect": "D:/CIENCIA-DE-DATOS-IA-4TO-CUATRIMESTRE/Practica-profecionalizantes-2/Sistema-BGH-Cable-Detection/BGH_PowerCheck/datasets/val/images/incorrect",
}

# Contar archivos e instancias
results = {}
for key, path in paths.items():
    if "labels" in key:
        results[key] = count_instances_in_labels(path)
    elif "images" in key:
        results[key] = count_files(path, extensions=('.jpg', '.png'))

# Mostrar resultados
for key, count in results.items():
    print(f"{key}: {count}")
