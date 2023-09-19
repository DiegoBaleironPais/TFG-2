import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

# Cargar el modelo previamente guardado
modelo = load_model('ModeloEntrenado/number_preditor.h5')

# Función para procesar una nueva imagen
def procesar_imagen(ruta_imagen):
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((48, 53))
    imagen = np.array(imagen)
    imagen = imagen.reshape((-1, 48, 53, 1))
    imagen = imagen / 255.0
    return imagen

# Función para predecir el número en una imagen
def predecir_numero(ruta_imagen):
    imagen_procesada = procesar_imagen(ruta_imagen)
    predicciones = modelo.predict(imagen_procesada)
    numero_predicho = np.argmax(predicciones, axis=1)[0]
    
    # Ajuste para obtener el número original
    numero_predicho += 1
    if numero_predicho > 7:
        numero_predicho += 2

    return numero_predicho

# Usa la función para predecir números en nuevas imágenes
ruta_nueva_imagen = "ConjuntoEntrenamiento/1_4.jpg"
numero = predecir_numero(ruta_nueva_imagen)
print(f"El número predicho en la imagen es: {numero}")