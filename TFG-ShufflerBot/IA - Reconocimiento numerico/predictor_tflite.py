import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

def load_image(ruta_imagen):
    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((48, 53))
    imagen = np.array(imagen).astype(np.float32)
    imagen = imagen / 255.0
    imagen = imagen.reshape((-1, 48, 53, 1))
    return imagen

def predict_with_tflite(tflite_model_path, image_path):
    print("Hasta aqui si")
    # Cargar el modelo TFLite
    interpreter = tflite.Interpreter(model_path=tflite_model_path)
    print("Hasta aqui si")
    interpreter.allocate_tensors()

    # Obtener entradas y salidas del modelo
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Cargar y procesar la imagen
    image = load_image(image_path)

    # Ejecutar inferencia
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])

    # Obtener el número predicho
    numero_predicho = np.argmax(predictions, axis=1)[0]
    
    # Ajuste para obtener el número original
    numero_predicho += 1
    if numero_predicho > 7:
        numero_predicho += 2

    return numero_predicho

# Usar la función para predecir
ruta_modelo_tflite = "./number_preditor.tflite"
ruta_imagen = "ConjuntoEntrenamiento/1_4.jpg"
numero = predict_with_tflite(ruta_modelo_tflite, ruta_imagen)
print(f"El número predicho en la imagen es: {numero}")
