import serial
import sys
import time

# Variables globales
tiempo_ultima_orden = 0
numero_inserciones = 0
encendido = True

class ControladorDispensador:
    def __init__(self):
        global tiempo_ultima_orden
        global encendido
        try:
            self.dispenser_serial = serial.Serial('/dev/ttyACM1', 9600)
            print("Dispensador conectado con éxito")
            self.dispenser_serial.write(b's')
            encendido = True
        except serial.SerialException as e:
            print(f"No se pudo abrir el puerto serial: {e}")
            sys.exit(1)
        tiempo_ultima_orden = time.time()


    def dispensar_carta(self):
        global tiempo_ultima_orden, numero_inserciones

        # Esperar si la última orden fue hace menos de 1.8 segundos
        tiempo_actual = time.time()
        if tiempo_actual - tiempo_ultima_orden < 1.8:
            time.sleep(1.8 - (tiempo_actual - tiempo_ultima_orden))

        # Enviar comando por el puerto serial
        self.dispenser_serial.write(b'n')

        # Actualizar el número de inserciones y el tiempo de la última orden
        numero_inserciones += 1
        tiempo_ultima_orden = time.time()

    def encender_motor(self):
        # Similar a dispensar_carta, pero envía el comando para encender el motor
        global tiempo_ultima_orden, numero_inserciones, encendido

        tiempo_actual = time.time()
        if tiempo_actual - tiempo_ultima_orden < 1.8:
            time.sleep(1.8 - (tiempo_actual - tiempo_ultima_orden))

        # Enviar comando por el puerto serial
        self.dispenser_serial.write(b's')
        encendido = True

    def apagar_motor(self):
        # Similar a dispensar_carta, pero envía el comando para apagar el motor
        global tiempo_ultima_orden, numero_inserciones, encendido

        tiempo_actual = time.time()
        if tiempo_actual - tiempo_ultima_orden < 1.8:
            time.sleep(1.8 - (tiempo_actual - tiempo_ultima_orden))

        # Enviar comando por el puerto serial
        self.dispenser_serial.write(b't')
        encendido = False


    def motor_encendido(self):
        # Devuelve el estado actual del motor (encendido o apagado)
        global encendido
        return encendido

