from PIL import Image
import pytesseract
import re

# Configura el path de tesseract si no está en tu PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ajusta según tu instalación

# Cargar la imagen
img = Image.open('min.jpg')

# Extraer texto de la imagen
texto = pytesseract.image_to_string(img)

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
