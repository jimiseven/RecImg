import cv2
import os
import numpy as np
from PIL import Image
from imagehash import phash
import pytesseract
import mediapipe as mp

# Ruta al ejecutable de Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Configuración de MediaPipe para detección de rostros
mp_face_detection = mp.solutions.face_detection

def extraer_diapositivas_mejorado(video_path, output_folder, umbral=100000, min_distancia=30):
    """
    Extrae diapositivas únicas de un video detectando cambios significativos en los cuadros.
    Filtra imágenes que contienen rostros y verifica si contienen texto usando OCR.
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
    saved_hashes = set()  # Para almacenar los hashes de las imágenes guardadas

    # Inicializar detección de rostros
    face_detector = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.6)

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
                # Filtrar imágenes con rostros
                if contiene_rostros(face_detector, frame):
                    print(f"Saltando cuadro {frame_count}: contiene rostros.")
                    continue

                # Verificar si contiene texto (OCR)
                if not contiene_texto(frame):
                    print(f"Saltando cuadro {frame_count}: no contiene texto.")
                    continue

                # Generar hash perceptual del fotograma
                frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                frame_hash = phash(frame_pil)

                # Comprobar si ya se ha guardado una imagen similar
                if frame_hash not in saved_hashes:
                    output_path = os.path.join(output_folder, f"diapositiva_{saved_count}.jpg")
                    cv2.imwrite(output_path, frame)
                    saved_hashes.add(frame_hash)
                    print(f"Guardando: {output_path}")
                    saved_count += 1
                    last_saved_frame = frame_count

        # Actualizar el frame anterior
        prev_frame = gray_frame
        frame_count += 1

    cap.release()
    print(f"Extracción completada. Se guardaron {saved_count} diapositivas.")

def contiene_rostros(face_detector, frame):
    """
    Detecta si un fotograma contiene rostros.
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_detector.process(rgb_frame)
    return results.detections is not None  # Devuelve True si se detectaron rostros

def contiene_texto(frame):
    """
    Verifica si un fotograma contiene texto utilizando OCR.
    """
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    texto = pytesseract.image_to_string(gray_frame)
    return len(texto.strip()) > 5  # Considera relevante si se detecta más de 5 caracteres de texto

def eliminar_imagenes_repetidas(folder_path, threshold=0.95):
    """
    Revisa las imágenes en una carpeta y elimina las que sean visualmente similares.
    """
    imagenes = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jpg')]
    imagenes.sort()
    eliminadas = 0

    for i in range(len(imagenes) - 1):
        img1 = cv2.imread(imagenes[i], cv2.IMREAD_GRAYSCALE)
        
        for j in range(i + 1, len(imagenes)):
            if not os.path.exists(imagenes[j]):
                continue
            
            img2 = cv2.imread(imagenes[j], cv2.IMREAD_GRAYSCALE)
            img1_resized = cv2.resize(img1, (300, 300))
            img2_resized = cv2.resize(img2, (300, 300))

            # Calcular la similitud estructural (SSIM)
            ssim_score, _ = compare_ssim(img1_resized, img2_resized, full=True)
            if ssim_score > threshold:
                print(f"Eliminando imagen similar: {imagenes[j]} (Similitud: {ssim_score:.2f})")
                os.remove(imagenes[j])
                eliminadas += 1

    print(f"Total de imágenes eliminadas: {eliminadas}")

# Configuración
video_path = "../reset/vid/vi2.mp4"  # Ruta del video
output_folder = "../reset/diapos3"  # Carpeta donde guardarás las imágenes
umbral = 100000  # Ajusta este valor si detecta muchas o pocas imágenes
min_distancia = 30  # Asegúrate de guardar cuadros separados por al menos este número de cuadros

# Ejecutar el proceso
extraer_diapositivas_mejorado(video_path, output_folder, umbral, min_distancia)
eliminar_imagenes_repetidas(output_folder)
