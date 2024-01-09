from definitions import PI_CAM_ID, USB_CAM_ID
import base64
import io
import picamera
import picamera.array
import cv2

class ControladorRecon:
    '''
    Clase que permite identificar cartas con dos cámaras diferentes.

    Atributos
    ----------
    cam_pi : picamera.PiCamera
        Variable que controla la PiCamera.
    captura_raw_pi : picamera.array.PiRGBArray
        Variable utilizada para obtener fácilmente un arreglo numpy tridimensional de la PiCamera.
    cam_usb : cv2.VideoCapture
        Variable que controla la USBCamera.
    '''

    def __init__(self):
        # Utilizar los identificadores de cámara definidos en definitions.py
        self.ID_CAM_PI = PI_CAM_ID
        self.ID_CAM_USB = USB_CAM_ID
        self.cam_pi = None
        self.captura_raw_pi = None
        self.cam_usb = None

    def iniciar_camara(self, camara):
        if camara == 0:  # Para PiCamera
            self.cam_pi = picamera.PiCamera()
            self.captura_raw_pi = picamera.array.PiRGBArray(self.cam_pi)

        elif camara == 1:  # Para USBCamera
            self.cam_usb = cv2.VideoCapture(0)

    def detener_camara(self, camara):
        if camara == 0:  # Para PiCamera
            self.cam_pi.close()

        elif camara == 1:  # Para USBCamera
            self.cam_usb.release()

    @app.route('/capturar_imagen', methods=['GET'])
    def capturar_imagen():
        camara = int(request.args.get('camara', type=int))
        imagen = controlador.capturar_imagen(camara)

        if imagen is not None:
            # Convertir la imagen a formato JPEG (u otro formato de tu elección)
            _, buffer = cv2.imencode('.jpg', imagen)
            # Codificar la imagen en base64 y decodificar a cadena para JSON
            imagen_codificada = base64.b64encode(buffer).decode()

            return jsonify({'mensaje': 'Imagen capturada', 'imagen': imagen_codificada}), 200
        else:
            return jsonify({'mensaje': 'No se pudo capturar la imagen'}), 500
