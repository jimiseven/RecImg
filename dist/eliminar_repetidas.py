import os
import cv2
from skimage.metrics import structural_similarity as compare_ssim

def eliminar_imagenes_repetidas(folder_path, threshold=0.95):
    """
    Analiza las imágenes en una carpeta y elimina las que son repetidas basándose en similitud estructural (SSIM).
    
    :param folder_path: Ruta de la carpeta que contiene las imágenes.
    :param threshold: Umbral de similitud para considerar dos imágenes como repetidas (0.0 a 1.0).
    """
    # Obtener la lista de imágenes en la carpeta
    imagenes = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]
    imagenes.sort()  # Procesarlas en orden
    total_eliminadas = 0

    for i in range(len(imagenes)):
        if not os.path.exists(imagenes[i]):
            continue  # Saltar si la imagen ya fue eliminada
        
        img1 = cv2.imread(imagenes[i], cv2.IMREAD_GRAYSCALE)

        for j in range(i + 1, len(imagenes)):
            if not os.path.exists(imagenes[j]):
                continue  # Saltar si la imagen ya fue eliminada
            
            img2 = cv2.imread(imagenes[j], cv2.IMREAD_GRAYSCALE)

            # Cambiar el tamaño de las imágenes para garantizar comparabilidad
            img1_resized = cv2.resize(img1, (300, 300))
            img2_resized = cv2.resize(img2, (300, 300))

            # Calcular la similitud estructural (SSIM)
            ssim_score, _ = compare_ssim(img1_resized, img2_resized, full=True)

            # Si las imágenes son similares, eliminar la segunda
            if ssim_score > threshold:
                print(f"Eliminando imagen similar: {imagenes[j]} (Similitud: {ssim_score:.2f})")
                os.remove(imagenes[j])
                total_eliminadas += 1

    print(f"Proceso finalizado. Total de imágenes eliminadas: {total_eliminadas}")

# Configuración
folder_path = "../reset/diapos2"  # Cambia esto por la ruta de tu carpeta con imágenes
threshold = 0.95  # Ajusta este valor según el nivel de similitud deseado (0.95 es muy estricto)

eliminar_imagenes_repetidas(folder_path, threshold)
