import requests
import os

# HTTP request al microservicio y recogida del JSON de respuesta
def send_image_to_server(image_path, server_url):
    with open(image_path, 'rb') as img_file:
        files = {'file': img_file}
        response = requests.post(server_url, files=files)
        return response.json()

def main():
    # URL del microservicio Flask
    SERVER_URL = "http://192.168.1.153:5000/predict"
    
    # Ruta de la imagen a enviar
    IMAGE_PATH = "path_to_your_image.jpg"  
    
    response = send_image_to_server(IMAGE_PATH, SERVER_URL)
    
    # Extraccion del valor de la imagen
    image_name = os.path.basename(IMAGE_PATH)
    true_number = int(image_name.split('_')[0])
    
    # Comparacion con la respuesta del servidor
    predicted_number = response.get('number')
    
    if predicted_number == true_number:
        print(f"¡Correcto! Predicción: {predicted_number}, Real: {true_number}")
    else:
        print(f"Incorrecto. Predicción: {predicted_number}, Real: {true_number}")

if __name__ == "__main__":
    main()
