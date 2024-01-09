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
        '''
        Inicia la captura con la cámara dada.

        Parámetros
        ----------
        camara : int
            La cámara con la que iniciar la captura.
        '''
        # Si queremos iniciar la captura con la PiCamera
        if camara == self.ID_CAM_PI:
            self.cam_pi = picamera.PiCamera()
            self.captura_raw_pi = picamera.array.PiRGBArray(self.cam_pi)

        # Si queremos iniciar la captura con la USBCamera
        elif camara == self.ID_CAM_USB:
            self.cam_usb = cv2.VideoCapture(0)
            
    def detener_camara(self, camara):
        '''
        Detiene la captura con la cámara dada.

        Parámetros
        ----------
        camara : int
            La cámara con la que detener la captura.
        '''
        # Si queremos detener la captura con la PiCamera
        if camara == self.ID_CAM_PI:
            self.cam_pi.close()

        # Si queremos detener la captura con la USBCamera
        elif camara == self.ID_CAM_USB:
            self.cam_usb.release()

    def capturar_imagen(self, camara):
        '''
        Captura una imagen con la cámara dada.

        Parámetros
        ----------
        camara : int
            La cámara con la que capturar la imagen.

        Devuelve
        -------
        imagen : numpy.ndarray
            La imagen capturada.
        '''
        # Si queremos capturar con la PiCamera
        if camara == self.ID_CAM_PI:
            self.cam_pi.capture(self.captura_raw_pi, format="bgr")
            imagen = self.captura_raw_pi.array
            self.captura_raw_pi.truncate(0)

        # Si queremos capturar con la USBCamera
        elif camara == self.ID_CAM_USB:
            _, imagen = self.cam_usb.read()

        # Devolver la imagen capturada
        return imagen
    
def main():
    # Crear una instancia del identificador de cartas
    identificador = ControladorRecon()

    # Elegir qué cámara iniciar (0 para PiCamera, 1 para USBCamera)
    camara_para_iniciar = 0  # Cambia este valor dependiendo de la cámara que quieras usar

    # Iniciar la cámara seleccionada
    identificador.iniciar_camara(camara_para_iniciar)

    # Realizar una captura con la cámara seleccionada
    imagen_capturada = identificador.capturar_imagen(camara_para_iniciar)

    # Aquí puedes procesar la imagen capturada según tus necesidades
    # Por ejemplo, puedes mostrar la imagen usando OpenCV
    # cv2.imshow("Captura", imagen_capturada)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Detener la cámara
    identificador.detener_camara(camara_para_iniciar)

if __name__ == "__main__":
    main()