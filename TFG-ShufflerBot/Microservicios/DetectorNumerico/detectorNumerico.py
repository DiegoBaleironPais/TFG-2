from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Inicializacion de Flask
app = Flask(__name__)

# Cargado del modelo previamente entrenado
model = load_model('number_preditor.h5')
print("Modelo cargado con exito!!!!")

# Creación del endpoint para recibir imagenes
@app.route('/predict', methods=['POST'])
def predict():
    # Checkeo de argumentos
    if 'file' not in request.files:
        return jsonify({'error': 'No se ha enviado ninguna imagen'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se ha seleccionado ninguna imagen'}), 400

    try:
        # Lectura y preprocesado de la imagen
        image = Image.open(file).resize((48, 53))
        image = np.array(image).reshape((-1, 48, 53, 1))
        image = image / 255.0

        # Prediccion
        pred = model.predict(image)
        number = np.argmax(pred, axis=1)[0] + 1
        if number > 7:
            number += 2

        print("Número leido con exito, ", number)
        return jsonify({'number': int(number)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

#Inicio de la aplicacion
if __name__ == '__main__':
    app.run(debug=True)
