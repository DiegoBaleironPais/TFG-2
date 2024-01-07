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
        '/dispensar': 'Envía el comando para dispensar una carta',
        '/encender': 'Envía el comando para encender el motor',
        '/apagar': 'Envía el comando para apagar el motor',
        '/estado': 'Devuelve el estado actual del motor (encendido o apagado)'
    }
    return jsonify(descripcion)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)