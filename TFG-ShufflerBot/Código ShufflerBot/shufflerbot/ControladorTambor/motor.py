import time


class Motor:
    '''
    Objeto que permite controlar un motor paso a paso.
    
    Atributos
    ---------
    _id : int
        Variable 'privada' que identifica al motor.
    controlador : telemetrix.Telemetrix
        Variable utilizada para acceder a los métodos de la API de Telemetrix.
    num_pasos : int
        Número de pasos totales del motor.
    posicion_actual : int
        Paso en el que se encuentra el motor en este momento.
    motor_en_movimiento : bool
        Variable que indica si el motor está en movimiento o no en este momento.
    '''

    def __init__(self, controlador, pin_impulso, pin_direccion, num_pasos, vel_max, aceleracion):
        self._id = controlador.set_pin_mode_stepper(pin1=pin_impulso, pin2=pin_direccion)
        self.controlador = controlador
        self.num_pasos = num_pasos
        self.posicion_actual = 0
        self.motor_en_movimiento = False
        
        self.establecer_vel_max(vel_max)
        self.establecer_aceleracion(aceleracion)

    def establecer_posicion_actual(self, posicion_actual):
        '''
        Actualiza la posición actual del motor.

        Parámetros
        ----------
        posicion_actual : int
            Paso actual en el que se encuentra el motor.
        '''
        self.posicion_actual = posicion_actual
        self.controlador.stepper_set_current_position(self._id, posicion_actual)

    def establecer_vel_max(self, vel_max):
        '''
        Actualiza la velocidad máxima del motor.

        Parámetros
        ----------
        vel_max : int
            Velocidad máxima que el motor puede alcanzar en pasos por segundo.

        Lanza
        ------
        RuntimeError
            La velocidad máxima debe estar entre 1 y 1000 pasos por segundo.
        '''
        self._vel_max = vel_max
        self.controlador.stepper_set_max_speed(self._id, vel_max)

    def establecer_aceleracion(self, aceleracion):
        '''
        Actualiza la aceleración del motor.

        Parámetros
        ----------
        aceleracion : int
            Aceleración aplicada al motor en pasos por segundo al cuadrado.

        Lanza
        ------
        RuntimeError
            La aceleración debe estar entre 1 y 1000 pasos por segundo al cuadrado.
        '''
        self._aceleracion = aceleracion
        self.controlador.stepper_set_acceleration(self._id, aceleracion)

    def actualizar_estado_motor(self, datos_motor):
        '''
        Actualiza el estado del motor cuando ha terminado de girar.

        Parámetros
        ----------
        datos_motor : list
            Lista con los datos del último giro del motor.
        '''
        # Actualizar que el motor ya no está en movimiento.
        self.motor_en_movimiento = False

        # Registrar información sobre la rotación
        fecha = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(datos_motor[2]))
        print(f'{fecha}: Motor con id {datos_motor[1]} terminó de girar.')

    def girar(self, pasos):
        '''
        Gira el motor en relación a su posición actual.

        Parámetros
        ----------
        pasos : int
            Número de pasos a girar en sentido antihorario (pasos negativos para girar en sentido contrario).
        '''
        # Establecer el número de pasos a girar
        self.controlador.stepper_move(self._id, pasos)

        # Indicar que el motor está en movimiento
        self.motor_en_movimiento = True

        # Girar el motor el número de pasos deseado
        self.controlador.stepper_run(self._id, completion_callback=lambda datos_motor: self.actualizar_estado_motor(datos_motor))
        
        # Esperar a que el motor termine de girar
        while self.motor_en_movimiento:
            time.sleep(.1)

        # Actualizar la posición actual - mantenerla siempre en el rango [0, num_pasos)
        self.posicion_actual = (self.posicion_actual + pasos) % self.num_pasos
        self.controlador.stepper_set_current_position(self._id, self.posicion_actual)

    def girar_a(self, destino, sentido_horario=False):
        '''
        Gira el motor a una posición absoluta (en el rango [0, num_pasos)) en una dirección dada.

        Parámetros
        ----------
        destino : int
            Paso en el que el motor se detendrá.
        sentido_horario : boolean
            Dirección en la que el motor girará. True significa giro horario, y False, antihorario.
        '''                
        # Determinar el número de pasos a girar
        pasos_a_girar = destino - self.posicion_actual

        # Si usamos el método stepper_move_to, el motor siempre girará en la dirección que resulte en el giro más corto.
        # Para forzarlo de una manera fija, tenemos que añadir o restar una rotación completa y moverlo relativamente.
        if sentido_horario:
            pasos_a_girar %= -self.num_pasos
        
        else:
            pasos_a_girar %= self.num_pasos

        # Girar el motor
        self.girar(pasos_a_girar)

