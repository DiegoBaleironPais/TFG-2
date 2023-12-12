import RPi.GPIO as GPIO
import time

# Configuramos la GPIO por el número de pin en la placa
GPIO.setmode(GPIO.BOARD)

# Configuramos el pin 15 como entrada y habilitamos la resistencia de pull-down interna
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Configuramos un pin adicional como "enable" para el sensor (por ejemplo, pin 16)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.HIGH)  # Activamos el sensor

# Inicializamos el contador
contador_objetos = 0

try:
    while True:
        # Verificamos si el pin "enable" está en alto para proceder
        if GPIO.input(16) == GPIO.HIGH:
            if GPIO.input(15) == GPIO.LOW:  # Cuando el sensor se activa la salida es LOW
                # Incrementamos el contador cuando detectamos un objeto
                contador_objetos += 1
                print(f"Objeto detectado! Contador: {contador_objetos}")
                # Esperamos a que el objeto deje de ser detectado para evitar múltiples conteos
                while GPIO.input(15) == GPIO.LOW:
                    time.sleep(0.1)
            else:
                print("No hay objetos detectados.")
        else:
            print("Sensor deshabilitado.")
        
        # Esperamos un poco antes de leer de nuevo para evitar múltiples detecciones del mismo objeto
        time.sleep(0.1)

except KeyboardInterrupt:
    # Limpiamos la configuración al salir
    GPIO.cleanup()

# Imprimimos el total de objetos detectados al finalizar
print(f"Total de objetos detectados: {contador_objetos}")
