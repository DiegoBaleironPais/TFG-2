import serial

# Configura la conexión serial
port = '/dev/ttyACM0'  # Puerto serial del Arduino
baudrate = 9600        # Velocidad en baudios para la comunicación

# Intenta establecer la conexión serial
try:
    ser = serial.Serial(port, baudrate)
    print("Presiona cualquier tecla para enviar 'p'. Presiona Ctrl+C para salir.")

    while True:
        input("Presiona Enter para enviar 'p' y esperar respuesta.")
        ser.write(b'p')  # Enviar 'p' al Arduino

except serial.SerialException as e:
    print(f"Error al abrir el puerto serial: {e}")
except KeyboardInterrupt:
    print("\nPrograma terminado por el usuario.")
finally:
    ser.close()  # Asegúrate de cerrar la conexión serial
    print("Conexión serial cerrada.")

