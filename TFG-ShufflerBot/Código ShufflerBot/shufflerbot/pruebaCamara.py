import cv2

# Crear un objeto de captura de video.
# El argumento puede ser el índice de la cámara o el nombre del archivo de video.
cap = cv2.VideoCapture(0) 

while(True):
    # Capturar cuadro por cuadro
    ret, frame = cap.read()

    # Muestra el cuadro resultante
    cv2.imshow('Frame', frame)

    # Si presionas 'q' en el teclado, el bucle while se romperá y la ventana de la cámara se cerrará.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cuando todo esté hecho, liberar la captura de video y destruir todas las ventanas
cap.release()
cv2.destroyAllWindows()

