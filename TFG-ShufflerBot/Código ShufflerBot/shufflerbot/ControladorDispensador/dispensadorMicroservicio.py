from flask import Flask, jsonify, request
from ControladorDispensador import ControladorDispensador  # Asegúrate de que ControladorDispensador esté en un módulo accesible

app = Flask(__name__)

# Instancia del controlador
dispensador = ControladorDispensador()

@app.route('/dispensar', methods=['POST'])
def dispensar():
    dispensador.dispensar_carta()
    return jsonify({'mensaje': 'Carta dispensada'})

@app.route('/encender', methods=['POST'])
def encender():
    dispensador.encender_motor()
    return jsonify({'mensaje': 'Motor encendido'})

@app.route('/apagar', methods=['POST'])
def apagar():
    dispensador.apagar_motor()
    return jsonify({'mensaje': 'Motor apagado'})

@app.route('/estado', methods=['GET'])
def estado():
    estado = dispensador.motor_encendido()
    return jsonify({'encendido': estado})

@app.route('/describe', methods=['GET'])
def describe():
    descripcion = {
        '/dispensar': {
            'metodo': 'POST',
            'descripcion': 'Envía el comando para dispensar una carta.',
            'url': '/dispensar',
            'parametros_entrada': None,
            'parametros_salida': {'mensaje': 'Carta dispensada'}
        },
        '/encender': {
            'metodo': 'POST',
            'descripcion': 'Envía el comando para encender el motor del dispensador.',
            'url': '/encender',
            'parametros_entrada': None,
            'parametros_salida': {'mensaje': 'Motor encendido'}
        },
        '/apagar': {
            'metodo': 'POST',
            'descripcion': 'Envía el comando para apagar el motor del dispensador.',
            'url': '/apagar',
            'parametros_entrada': None,
            'parametros_salida': {'mensaje': 'Motor apagado'}
        },
        '/estado': {
            'metodo': 'GET',
            'descripcion': 'Consulta el estado actual del motor del dispensador (encendido o apagado).',
            'url': '/estado',
            'parametros_entrada': None,
            'parametros_salida': {'encendido': 'Estado actual del motor'}
        }
    }
    
    return jsonify(descripcion)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)