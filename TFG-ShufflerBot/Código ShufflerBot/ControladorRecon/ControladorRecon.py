from definitions import PI_CAM_ID, USB_CAM_ID
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

    def capturar_imagen(self, camara):
        if camara == 0:  # Para PiCamera
            self.cam_pi.capture(self.captura_raw_pi, format="bgr")
            imagen = self.captura_raw_pi.array
            self.captura_raw_pi.truncate(0)

        elif camara == 1:  # Para USBCamera
            _, imagen = self.cam_usb.read()

        return imagen