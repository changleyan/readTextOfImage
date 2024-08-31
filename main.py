import re
import cv2
import numpy as np
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def mejorar_imagen(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    return opening


def extraer_texto_y_numeros(ruta_imagen, palabra_buscar):
    img = cv2.imread(ruta_imagen)
    img_original = img.copy()

    resultados = []

    # Lista de técnicas de preprocesamiento
    tecnicas = [
        ("Original", lambda x: x),
        ("Mejorada", mejorar_imagen),
        ("Umbral",
         lambda x: cv2.threshold(cv2.cvtColor(x, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1])
    ]

    for nombre_tecnica, func_tecnica in tecnicas:
        img_procesada = func_tecnica(img_original)
        img_pil = Image.fromarray(
            img_procesada if len(img_procesada.shape) == 2 else cv2.cvtColor(img_procesada, cv2.COLOR_BGR2RGB))

        # Probar diferentes configuraciones de Tesseract
        configuraciones = [
            '--oem 3 --psm 6 -c preserve_interword_spaces=1',
            '--oem 3 --psm 11 -c preserve_interword_spaces=1',
            '--oem 3 --psm 4 -c preserve_interword_spaces=1'
        ]

        for config in configuraciones:
            texto = pytesseract.image_to_string(img_pil, config=config)
            print(f"\nTexto extraído ({nombre_tecnica}, config: {config}):")
            print(texto)

            # Buscar ocurrencias con un patrón más flexible
            patron = r'(?:Count|Gount|Count)[:.]?\s*(\d+)'
            numeros = re.findall(patron, texto, re.IGNORECASE)
            numeros = [int(num) for num in numeros]

            resultados.append((nombre_tecnica, config, numeros))

    # Encontrar el resultado con más coincidencias
    mejor_resultado = max(resultados, key=lambda x: len(x[2]))

    print(f"\nMejor resultado - Técnica: {mejor_resultado[0]}, Config: {mejor_resultado[1]}")
    print(f"Números encontrados: {mejor_resultado[2]}")

    return mejor_resultado[2]


# Uso de la función
ruta_imagen = 'max.jpg'
palabra_buscar = 'Count:'

numeros_encontrados = extraer_texto_y_numeros(ruta_imagen, palabra_buscar)