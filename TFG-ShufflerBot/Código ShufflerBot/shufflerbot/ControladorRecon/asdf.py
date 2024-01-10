import requests
import base64
import numpy as np
import cv2

# URL del microservicio para capturar la imagen
url = 'http://192.168.1.22:5002/capturar_imagen?camara=0'  # Asegúrate de usar la URL correcta

# Realizar la solicitud GET
respuesta = requests.get(url)

# Verificar si la solicitud fue exitosa
if respuesta.status_code == 200:
    # Extraer la imagen codificada en base64 del JSON de respuesta
    data_base64 = respuesta.json()['imagen']

    # Decodificar la cadena base64
    img_data = base64.b64decode(data_base64)

    # Convertir los datos en un array numpy
    nparr = np.frombuffer(img_data, np.uint8)

    # Convertir el array numpy en una imagen
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Mostrar la imagen
    cv2.imshow("Imagen Capturada", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Error en la solicitud:", respuesta.status_code)



