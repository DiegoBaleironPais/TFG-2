from flask import Flask, request, jsonify
from ControladorTambor import ControladorTambor  

app = Flask(__name__)

# Instancia de tu controlador
tambor = ControladorTambor()

@app.route('/describe', methods=['GET'])
def describe():
    descripcion = {
        'resetear': {
            'metodo': 'GET',
            'descripcion': 'Resetea la posición del tambor a su origen.',
            'url': '/resetear',
            'parametros_entrada': None,
            'parametros_salida': {'mensaje': 'Descripción del resultado'}
        },
        'barajar': {
            'metodo': 'GET',
            'descripcion': 'Baraja las cartas y devuelve las nuevas posiciones.',
            'url': '/barajar',
            'parametros_entrada': None,
            'parametros_salida': {'posiciones': 'Listado de las nuevas posiciones de las cartas'}
        },
        'insertar': {
            'metodo': 'POST',
            'descripcion': 'Inserta una carta en una posición específica.',
            'url': '/insertar',
            'parametros_entrada': {
                'carta': 'Identificador de la carta',
                'numero_carta': 'Número original de la carta en el mazo',
                'posicion_ranura': 'Posición en la que se insertará la carta'
            },
            'parametros_salida': {'mensaje': 'Descripción del resultado'}
        },
        'repartir': {
            'metodo': 'POST',
            'descripcion': 'Reparte una carta específica.',
            'url': '/repartir',
            'parametros_entrada': {'carta': 'Identificador de la carta a repartir'},
            'parametros_salida': {'mensaje': 'Descripción del resultado'}
        },
        'informacion_tambor': {
            'metodo': 'GET',
            'descripcion': 'Devuelve la información actual de todas las cartas en el tambor, incluyendo las posiciones vacías.',
            'url': '/informacion_tambor',
            'parametros_entrada': None,
            'parametros_salida': {'informacion': 'Listado del estado de cada posición en el tambor'}
        },
        'estado_fotosensor_salida': {
            'metodo': 'GET',
            'descripcion': 'Consulta el estado actual del fotosensor de salida.',
            'url': '/estado_fotosensor_salida',
            'parametros_entrada': None,
            'parametros_salida': {'estado_fotosensor_salida': 'Estado actual del fotosensor (True o False)'}
        }
    }
    
    return jsonify(descripcion)

@app.route('/resetear', methods=['GET'])
def resetear():
    tambor.resetear_posicion()
    return jsonify({'mensaje': 'Posición reseteada con éxito'})

@app.route('/barajar', methods=['GET'])
def barajar():
    posiciones = tambor.barajar()
    return jsonify({'posiciones': posiciones})

@app.route('/insertar', methods=['POST'])
def insertar_carta():
    datos = request.json
    carta = datos['carta']
    numero_carta = datos['numero_carta']
    posicion_ranura = datos['posicion_ranura']
    tambor.insertar_siguiente_carta(carta, numero_carta, posicion_ranura)
    return jsonify({'mensaje': f'Carta {carta} insertada en la posición {posicion_ranura}'})

@app.route('/repartir', methods=['POST'])
def repartir_carta():
    datos = request.json
    carta = datos['carta']
    tambor.repartir_carta(carta)
    return jsonify({'mensaje': f'Carta {carta} repartida'})

@app.route('/informacion_tambor', methods=['GET'])
def informacion_tambor():
    informacion = tambor.informacion_tambor()
    return jsonify({'informacion': informacion})

@app.route('/estado_fotosensor_salida', methods=['GET'])
def estado_fotosensor_salida():
    estado = tambor.consultar_estado_fotosensor_salida()
    return jsonify({'estado_fotosensor_salida': estado})

if __name__ == '__main__':
    app.run(debug=False,  host='0.0.0.0')