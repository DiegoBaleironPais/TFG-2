# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from ControladorRecon import ControladorRecon 

app = Flask(__name__)
controlador = ControladorRecon()

@app.route('/describe', methods=['GET'])
def describe():
    descripcion = {
        '/iniciar_camara': {
            'metodo': 'POST',
            'descripcion': 'Inicia la captura con la cámara especificada.',
            'url': '/iniciar_camara',
            'parametros_entrada': {'camara': 'Identificador de la cámara a iniciar (PI_CAM o USB_CAM)'},
            'parametros_salida': {'mensaje': 'Cámara iniciada'}
        },
        '/detener_camara': {
            'metodo': 'POST',
            'descripcion': 'Detiene la captura con la cámara especificada.',
            'url': '/detener_camara',
            'parametros_entrada': {'camara': 'Identificador de la cámara a detener (PI_CAM o USB_CAM)'},
            'parametros_salida': {'mensaje': 'Cámara detenida'}
        },
        '/capturar_imagen': {
            'metodo': 'GET',
            'descripcion': 'Captura una imagen con la cámara especificada.',
            'url': '/capturar_imagen',
            'parametros_entrada': {'camara': 'Identificador de la cámara para capturar la imagen (PI_CAM o USB_CAM)'},
            'parametros_salida': {'mensaje': 'Imagen capturada'}
        }
    }

    return jsonify(descripcion)

@app.route('/iniciar_camara', methods=['POST'])
def iniciar_camara():
    data = request.json
    camara = int(data.get('camara'))  # Convertir a int
    controlador.iniciar_camara(camara)
    return jsonify({'mensaje': 'Cámara iniciada'}), 200

@app.route('/detener_camara', methods=['POST'])
def detener_camara():
    data = request.json
    camara = int(data.get('camara'))  # Asegúrate de convertir a entero
    controlador.detener_camara(camara)
    return jsonify({'mensaje': 'Cámara detenida'}), 200

@app.route('/capturar_imagen', methods=['GET'])
def capturar_imagen():
    camara = int(request.args.get('camara', type=int))  # Asegúrate de convertir a entero
    imagen = controlador.capturar_imagen(camara)
    # Manejo adicional si quieres devolver la imagen o guardarla
    return jsonify({'mensaje': 'Imagen capturada'}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5002)