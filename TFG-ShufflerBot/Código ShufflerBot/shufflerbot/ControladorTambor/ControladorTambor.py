import time
import telemetrix

from motor import Motor
from random import randint
from definitions import *

# Variable que contiene si el fotosensor ha detectado algo
fotosensor_barajador = False
fotosensor_dispensador = False
carta_insertada = False

# Función de callback para recibir una notificación cuando el fotosensor detecta algo
def callback_fotosensor_barajador(datos):
    
    if datos[2] == 0:
        
        # Indicar que el fotosensor ha detectado algo
        global fotosensor_barajador
        fotosensor_barajador = True

        # Mostrar información sobre la detección
        fecha = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(datos[3]))
        print(f"{fecha}: Fotosensor ha detectado algo.")


class ControladorTambor:
    '''
    Objeto que actúa como un almacenamiento de cartas, reparte y juega las cartas.

    Atributos
    ----------
    controlador : telemetrix.Telemetrix
        Variable usada para acceder a los métodos de la API de Telemetrix.
    motor_principal : motor.Motor
        Motor adjunto al almacenamiento.
    pin_fotoBarajador : int
        Número del pin al que está conectado el fotosensor del barajador.
    mazo : list
        Las cartas que tiene el mazo.
    tipo_barajado : int
        El tipo de barajado.
    paso_extractor : int
        El paso en el que se encuentra la rampa del extractor.
    num_cartas : int
        Capacidad de cartas del almacenamiento.
    pasos_por_posicion : int
        Número de pasos del motor que corresponden a cada posición.
    cartas: list
        Lista que contiene todas las cartas en el almacenamiento: El mazo barajado.
    ranuras : list
        Lista que contiene la ranura de cada carta en el almacenamiento.
    '''

    def __init__(self):
        # Inicializar el controlador con el puerto correcto
        self.controlador = telemetrix.Telemetrix(com_port='/dev/ttyACM0')
        
        # Configurar el pin del motor como salida y deshabilitarlo inicialmente
        self.controlador.set_pin_mode_digital_output(ENABLE_PIN)
        self.controlador.digital_write(ENABLE_PIN, 0)
        
        # Asignar el motor principal con los ajustes definidos en definitions.py
        self.motor_principal = Motor(STORAGE_PULSE_PIN, STORAGE_DIRECTION_PIN, STORAGE_NUM_STEPS, STORAGE_MAX_SPEED, STORAGE_ACCELERATION)
        
        # Asignar pin del fotosensor barajador usando las constantes de definitions.py
        self.pin_fotoBarajador = PHOTOSENSOR_PIN
        
        # Asignar mazo y tipo de barajado desde definitions.py
        self.mazo = DECK
        self.tipo_barajado = ORDERED_SHUFFLE  # O CHAOTIC_SHUFFLE según lo que necesites
        
        # Paso del extractor también desde definitions.py
        self.paso_extractor = EXTRACTOR_STEP
        
        # Calcular el número de cartas y los pasos por ranura
        self.num_cartas = len(self.mazo)
        self.pasos_por_ranura = self.motor_principal.num_pasos / self.num_cartas
        
        # Inicializar las listas de cartas y ranuras
        self.cartas = [None] * self.num_cartas
        self.ranuras = [None] * self.num_cartas

        # Configurar el fotosensor barajador para entrada digital y deshabilitar reportes
        self.controlador.set_pin_mode_digital_input(self.pin_fotoBarajador, callback_fotosensor_barajador)
        self.controlador.disable_digital_reporting(self.pin_fotoBarajador)

    def resetear_posicion(self):
        '''
        Gira el almacenamiento a su origen, posición 0.
        '''
        # Variable que verifica si el almacenamiento está en el origen
        global fotosensor_barajador
        fotosensor_barajador = False

        # Habilitar el fotosensor
        self.controlador.enable_digital_reporting(self.pin_fotoBarajador)

        # Girar motor mientras no esté en la posición correcta
        while not fotosensor_barajador:
            self.motor_principal.girar(2)
            
        # Una vez en la posición correcta, establecer la posición del almacenamiento en 0
        self.motor_principal.establecer_posicion_actual(2)

        # Deshabilitar el fotosensor
        self.controlador.disable_digital_reporting(self.pin_fotoBarajador)

    def insertar_siguiente_carta(self, carta, numero_carta, posicion):
        '''
        Inserta una carta en una posición dada del almacenamiento.

        Parámetros
        ----------
        carta : string
            Carta a insertar.
        numero_carta : int
            Dónde estaba la carta en el mazo no barajado.
        posicion_ranura : int
            Posición de la ranura en la que se insertará la siguiente carta.
        '''
        # Determinar la ranura de la carta

        # Barajado Ordenado
        if self.tipo_barajado == ORDERED_SHUFFLE:
            self.ranuras[posicion] = posicion
            posicion_ranura = int(posicion * self.pasos_por_ranura)

        # Barajado Caótico
        else:
            self.ranuras[posicion] = numero_carta
            posicion_ranura = int(numero_carta * self.pasos_por_ranura)

        # Añadir la carta al mazo actual en su posición determinada
        self.cartas[posicion] = carta
        
        # Girar el almacenamiento a la posición determinada
        self.motor_principal.girar_a(posicion_ranura)

    def barajar(self):
        '''
        Baraja las cartas e inserta en el almacenamiento.

        Devuelve
        -------
        posiciones : list
            Posiciones aleatorias donde irán las cartas.
        '''
        # Reiniciar el mazo actual
        self.cartas = [None] * self.num_cartas
        self.ranuras = [None] * self.num_cartas

        # Reiniciar la posición del almacenamiento
        self.resetear_posicion()
        
        # Obtener qué posición en el mazo tendrá cada carta.
        posiciones = list(range(self.num_cartas))
        
        # Para obtener posiciones completamente aleatorias, usamos el barajado de arriba-a-aleatorio:
        # - Tomar la primera posición y ponerla en un lugar aleatorio de la lista.
        # - A veces, esa posición puede ser después de la última. Cada vez que una nueva posición
        #   va después de la última (no el último elemento de la lista), tiene la misma oportunidad
        #   de estar en cualquier posición en ese subconjunto de ranuras. Por ejemplo, cuando solo una posición
        #   ha ido después de la última y llega una segunda, tiene 50% de estar antes o después de esa.
        # - Seguir haciendo esto hasta que la última posición sea el primer elemento de la lista.
        # - Terminamos poniendo esta última posición aleatoriamente en la lista.
        while posiciones[0] != (self.num_cartas - 1):
            posiciones.insert(randint(0, self.num_cartas - 1), posiciones.pop(0))
        posiciones.insert(randint(0, self.num_cartas - 1), posiciones.pop(0))

        return posiciones

    def repartir_carta(self, carta):
        '''
        Extrae la carta dada del almacenamiento.

        Parámetros
        ----------
        carta : string
            La carta a extraer.
        '''
        # Determinar en qué ranura está la carta a extraer
        ranura_carta = self.ranuras[self.cartas.index(carta)]

        # Obtener en qué paso está esa ranura
        paso_carta = (self.motor_principal.posicion_actual - ranura_carta * self.pasos_por_ranura) % self.motor_principal.num_pasos

        # Determinar cuántos pasos necesita girar el almacenamiento para poner la carta en la rampa del extractor
        pasos_hasta_extractor = self.paso_extractor - paso_carta

        # Finalmente, obtener en qué paso necesitamos rotar el almacenamiento teniendo en cuenta la rotación actual
        paso = self.motor_principal.posicion_actual + pasos_hasta_extractor
        
        # Rotar el almacenamiento a ese paso
        self.motor_principal.girar_a(int(paso))

        # Extraer la carta moviéndola de adelante hacia atrás
        self.motor_principal.girar(-7)
        self.motor_principal.girar(7)


if __name__ == "__main__":
    ControladorTambor = ControladorTambor()
    print("Reseteando la posición del tambor...")
    ControladorTambor.resetear_posicion()

    print("Insertando algunas cartas...")
    for i in range(5):  # Cambia el número según cuántas cartas quieras insertar
        carta = "12b"
        numero_carta = i
        posicion_ranura = i
        ControladorTambor.insertar_siguiente_carta(carta, numero_carta, posicion_ranura)
        print(f"Carta {carta} insertada en la posición {posicion_ranura}.")
