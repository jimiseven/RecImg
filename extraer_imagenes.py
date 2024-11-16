import cv2
import os
import numpy as np

def extraer_diapositivas_mejorado(video_path, output_folder, umbral=100000, min_distancia=30):
    """
    Extrae diapositivas únicas de un video detectando cambios significativos en los cuadros.
    Luego elimina imágenes repetidas basándose en similitud de histogramas.
    """
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Cargar el video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error al abrir el video.")
        return

    frame_count = 0
    saved_count = 0
    prev_frame = None
    last_saved_frame = -min_distancia  # Controlar la distancia mínima entre capturas

    while True:
        success, frame = cap.read()
        if not success:
            break  # Fin del video

        # Convertir el frame actual a escala de grises
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Comparar con el frame anterior
        if prev_frame is not None:
            # Calcular la diferencia absoluta entre los cuadros
            diff = cv2.absdiff(prev_frame, gray_frame)
            diff_score = np.sum(diff)

            # Si el cambio es significativo y se respeta la distancia mínima
            if diff_score > umbral and (frame_count - last_saved_frame) > min_distancia:
                output_path = os.path.join(output_folder, f"diapositiva_{saved_count}.jpg")
                cv2.imwrite(output_path, frame)
                print(f"Guardando: {output_path}")
                saved_count += 1
                last_saved_frame = frame_count

        # Actualizar el frame anterior
        prev_frame = gray_frame
        frame_count += 1

    cap.release()
    print(f"Extracción completada. Se guardaron {saved_count} diapositivas. Ahora eliminando duplicados...")

    eliminar_imagenes_repetidas(output_folder)
    print("Proceso finalizado. Las imágenes repetidas han sido eliminadas.")

def eliminar_imagenes_repetidas(folder_path, threshold=0.9):
    """
    Revisa las imágenes en la carpeta y elimina las que sean similares a otras ya guardadas.
    """
    # Obtener una lista de todas las imágenes en la carpeta
    imagenes = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]
    imagenes.sort()  # Asegurarse de procesarlas en orden

    eliminadas = 0
    for i in range(len(imagenes) - 1):
        img1 = cv2.imread(imagenes[i])
        hist1 = cv2.calcHist([img1], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist1 = cv2.normalize(hist1, hist1).flatten()

        for j in range(i + 1, len(imagenes)):
            img2 = cv2.imread(imagenes[j])
            hist2 = cv2.calcHist([img2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
            hist2 = cv2.normalize(hist2, hist2).flatten()

            # Calcular la similitud entre los histogramas
            similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            if similarity > threshold:
                print(f"Eliminando imagen similar: {imagenes[j]} (Similitud: {similarity:.2f})")
                os.remove(imagenes[j])
                eliminadas += 1

    print(f"Total de imágenes eliminadas: {eliminadas}")

# Configuración
video_path = "../reset/vid/vi1.mp4"  # Cambia esto por la ruta de tu video
output_folder = "../reset/diapos"  # Carpeta donde guardarás las imágenes
umbral = 100000  # Ajusta este valor si detecta muchas o pocas imágenes
min_distancia = 30  # Asegúrate de guardar cuadros separados por al menos este número de cuadros

extraer_diapositivas_mejorado(video_path, output_folder, umbral, min_distancia)
