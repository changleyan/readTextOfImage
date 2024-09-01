import easyocr
import cv2
import matplotlib.pyplot as plt
import re


def extract_text_from_image(image_path):
    # Inicializar el lector de EasyOCR
    reader = easyocr.Reader(['en'], gpu=False)

    # Leer el texto de la imagen
    result = reader.readtext(image_path)

    # Mostrar el texto detectado en la imagen
    image = cv2.imread(image_path)
    for (bbox, text, prob) in result:
        # Dibujar el recuadro de las palabras
        top_left = tuple([int(val) for val in bbox[0]])
        bottom_right = tuple([int(val) for val in bbox[2]])
        image = cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

        # Poner el texto reconocido en la imagen
        image = cv2.putText(image, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

    # Mostrar la imagen resultante
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    # Devolver el texto extraído
    extracted_text = ' '.join([text for (_, text, _) in result])
    return extracted_text


def find_numbers_after_count(text):
    # Reemplazar todos los ";" por ":"
    cleaned_text = text.replace(';', ':')

    # Buscar todas las ocurrencias de "Count:" y capturar el número que le sigue
    pattern = r"Count:\s*(\d+)"
    numbers = re.findall(pattern, cleaned_text)

    # Convertir las capturas a enteros y almacenarlos en un array
    numbers_array = [int(num) for num in numbers]
    return numbers_array


# Ruta de la imagen
image_path = 'max.jpg'

# Extraer texto de la imagen
extracted_text = extract_text_from_image(image_path)
print(f"Texto extraído: {extracted_text}")

# Buscar los números después de "Count:"
numbers = find_numbers_after_count(extracted_text)
print(f"Números encontrados: {numbers}")

# Usar la función sum() para obtener la suma de los elementos
suma = sum(numbers)

print("El total de casos es de:", suma)
