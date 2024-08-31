import re
import cv2
import numpy as np
from PIL import Image
import pytesseract

# Configura el path de tesseract si no está en tu PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Cargar la imagen
img = cv2.imread('min.jpg')

# Convertir a espacio de color HSV para una mejor segmentación del color
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Definir el rango de color para el blanco (ajustar según sea necesario)
lower_white = np.array([0, 0, 200], dtype=np.uint8)
upper_white = np.array([180, 20, 255], dtype=np.uint8)

# Crear una máscara para la hoja blanca
mask = cv2.inRange(hsv, lower_white, upper_white)

# Aplicar la máscara a la imagen original
res = cv2.bitwise_and(img, img, mask=mask)

# Convertir a escala de grises
gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

# Aplicar un umbral para mejorar el contraste del texto
_, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Encontrar contornos en la imagen binarizada
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Encontrar el contorno más grande que debería ser la hoja
max_contour = max(contours, key=cv2.contourArea)

# Crear un rectángulo que encierre el contorno más grande
x, y, w, h = cv2.boundingRect(max_contour)

# Recortar la imagen para obtener solo la hoja
cropped = img[y:y+h, x:x+w]

# Convertir a una imagen de PIL para usar con pytesseract
cropped_pil = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

# Extraer texto con pytesseract
custom_config = r'--oem 3 --psm 6'
texto = pytesseract.image_to_string(cropped_pil, config=custom_config)

# Imprimir el texto extraído
print("Texto extraído:")
print(texto)

# Buscar ocurrencias de la palabra y extraer números
palabra_buscar = 'Count:'  # Cambia esto por la palabra que buscas
patron = rf'{palabra_buscar}\D*(\d+)'  # Busca la palabra seguida de números

numeros = re.findall(patron, texto)

# Convertir los números encontrados a enteros
numeros = list(map(int, numeros))

# Imprimir los números extraídos
print("Números extraídos:")
print(numeros)
