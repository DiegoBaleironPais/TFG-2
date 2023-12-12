import picamera
import picamera.array
import cv2
import numpy as np
import pytesseract

class CardIdentifier:
    '''
    Class that allows to identify cards with to different cameras.

    Parameters
    ----------
    PI_CAM_ID : int
        Unique identifier of the PiCamera.
    USB_CAM_ID : int
        Unique identifier of the USBCamera.

    Attributes
    ----------
    PI_CAM_ID : int
        Unique identifier of the PiCamera.
    USB_CAM_ID : int
        Unique identifier of the USBCamera.
    pi_cam : picamera.PiCamera
        Variable that controls the PiCamera.
    pi_raw_capture : picamera.array.PiRGBArray
        Variable used to easily obtain a 3-dimensional numpy array from the PiCamera.
    usb_cam : cv2.VideoCapture
        Variable that controls the USBCamera.
    '''

    def __init__(self, PI_CAM_ID, USB_CAM_ID):
        self.PI_CAM_ID = PI_CAM_ID
        self.USB_CAM_ID = USB_CAM_ID
        self.pi_cam = None
        self.pi_raw_capture = None
        self.usb_cam = None

    def start_cam(self, camera):
        '''
        Starts capturing with the given camera

        Parameters
        ----------
        camera : int
            The camera to start capturing with.
        '''
        # If we want to start capturing with the PiCamera
        if camera == self.PI_CAM_ID:
            self.pi_cam = picamera.PiCamera()
            self.pi_raw_capture = picamera.array.PiRGBArray(self.pi_cam)

        # If we want to start capturing with the USBCamera
        elif camera == self.USB_CAM_ID:
            self.usb_cam = cv2.VideoCapture(0)
            
    def stop_cam(self, camera):
        '''
        Stops capturing with the given camera

        Parameters
        ----------
        camera : int
            The camera to stop capturing with.
        '''
        # If we want to stop capturing with the PiCamera
        if camera == self.PI_CAM_ID:
            self.pi_cam.close()

        # If we want to stop capturing with the USBCamera
        elif camera == self.USB_CAM_ID:
            self.usb_cam.release()

    def capture_image(self, camera):
        '''
        Captures an image with the given camera.

        Parameters
        ----------
        camera : int
            The camera to capture the image with.

        Returns
        -------
        image : numpy.ndarray
            The captured image.
        '''
        # If we want to capture with the PiCamera
        if camera == self.PI_CAM_ID:
            self.pi_cam.capture(self.pi_raw_capture, format="bgr")
            image = self.pi_raw_capture.array
            self.pi_raw_capture.truncate(0)

        # If we want to capture with the USBCamera
        elif camera == self.USB_CAM_ID:
            _, image = self.usb_cam.read()

        cv2.imwrite("Imagen Original.jpg",image)
        
        # Return the captured image
        return image
    
    def comprobar_inicio(self, image, y, x):
        height, width = image.shape
        for i in range(max(0, y - 20), min(height, y + 20)):
            if image[i, x] == 0:
                return False

        for j in range(x, min(width, x + 20)):
            if image[y, j] == 0:
                return True
        return False
    
    def buscar_pixeles_negros(self, image, y, image_width):
        # Inicializamos el contador de pixeles negros
        pixeles_negros = 0

        # Recorremos la imagen en la horizontal
        for x in range(image_width):
            # Recorremos el rango de altura
            for i in range(max(0, y - 10), min(image.shape[0], y+10)):
                # Si el pixel es negro, incrementamos el contador
                if image[i, x] == 0:
                    pixeles_negros += 1
                    break

        # Calculamos el porcentaje de pixeles negros
        porcentaje_pixeles_negros = (pixeles_negros / image_width) * 100

        return porcentaje_pixeles_negros

    def contar_segmentos(self, image, y, image_width):
        # Inicializamos el contador de segmentos
        segmentos = 0

        # Inicializamos una variable que nos indica si estamos en un segmento
        en_segmento = False

        # Inicializamos una variable que cuenta la longitud del segmento actual
        longitud_segmento = 0

        # Recorremos la imagen en la horizontal
        for x in range(image_width):
            # Asumimos que no hay píxeles negros en esta columna
            pixel_negro_en_columna = False

            # Recorremos el rango de altura
            for i in range(max(0, y - 5), min(image.shape[0], y + 10)):
                # Si encontramos un píxel negro, cambiamos la bandera
                if image[i, x] == 0:
                    pixel_negro_en_columna = True
                    break

            # Si encontramos un píxel negro y no estábamos en un segmento, empezamos uno nuevo
            if pixel_negro_en_columna and not en_segmento:
                en_segmento = True
                longitud_segmento = 1
            # Si encontramos un píxel negro y estábamos en un segmento, incrementamos la longitud
            elif pixel_negro_en_columna and en_segmento:
                longitud_segmento += 1
            # Si no encontramos un píxel negro y estábamos en un segmento, acabamos el segmento
            elif not pixel_negro_en_columna and en_segmento:
                if longitud_segmento >= 8:
                    segmentos += 1
                en_segmento = False

        return segmentos


    def prueba(self, image):
        #Conversion de la imagen a escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #Aplicacion del m�todo de OTSU para la binarizaci�n
        ret, otsu = cv2.threshold(gray, 55, 255, cv2.THRESH_BINARY)
        #Guardado de los resultados
        cv2.imwrite("Imagen a Grises.jpg", gray)
        cv2.imwrite("Imagen a Otsu.jpg", otsu)
        #Busqueda de la esquina superior izquierda de la carta
        image_height, image_width = otsu.shape
        altura_esquina = 0
        ancho_esquina = 0
        inicio_encontrado = False
        for x in range(image_width):
            for y in range(image_height):
                pixel = otsu[y, x]
                otsu[y, x] = 255
                if pixel == 0:
                    if not inicio_encontrado: 
                        inicio_encontrado = self.comprobar_inicio(otsu, y, x)
                    else:
                        altura_esquina = y
                        ancho_esquina = x
                        break
            if altura_esquina != 0:
                break

        #Medicion del porcentaje de negro en el segmento superior para identificar la carta
        porcentaje = self.buscar_pixeles_negros(otsu, altura_esquina, image_width)
        print("Porcentaje de pixeles negros: ", porcentaje, "%")
        if porcentaje > 55:
            palo = "Oros"
        #Conteo de segmentos para identificar la carta
        else:
            segmentos = self.contar_segmentos(otsu, altura_esquina, image_width)
            if segmentos == 2:
                palo = "Copas"
            elif segmentos == 3:
                palo = "Espadas"
            else:
                palo = "Bastos"
            
        
        #Aislamiento del n�mero de la carta
        numero_y_end = min(otsu.shape[0], altura_esquina + 55)
        numero_x_end = min(otsu.shape[1], ancho_esquina + 50)
        
        print("Dimensiones de la imagen:", otsu.shape)
        print("Altura esquina:", altura_esquina)
        print("Ancho esquina:", ancho_esquina)
        print("Numero Y end:", numero_y_end)
        print("Numero X end:", numero_x_end)

        # Recortamos la imagen
        numero_recortado = otsu[altura_esquina+2:numero_y_end, x+2:numero_x_end]
        #numero_concatenado = cv2.hconcat([numero_recortado, numero_recortado, numero_recortado, numero_recortado, numero_recortado])
        
        #scale_factor = 4
        #new_size = (numero_concatenado.shape[1] * scale_factor, numero_concatenado.shape[0] * scale_factor)
        #numero_escalado = cv2.resize(numero_concatenado, new_size)
        
        
        cv2.imwrite("NumeroRecortado.jpg", numero_recortado)
        
        #Reconocimiento de los numeros
        #number = pytesseract.image_to_string(numero_escalado, config='--dpi 200 tessedit_char_whitelist=01234567')
        
        # Elimina cualquier carácter que no sea un dígito
        #number = ''.join(char for char in number if char.isdigit())

        # Verifica la longitud del número y toma el último dígito si hay 3, o los dos últimos si hay 6
        #if len(number) == 5:
            #number = number[-1]
        #elif len(number) == 10:
            #number = number[-2:]

        
        for x in range(image_width):
            for y in range(max(0, altura_esquina - 20), min(image_height, altura_esquina+5)):
                otsu[y,x] = 125    

        cv2.imwrite("Imagen OtsuModificada.jpg", otsu)
        return "7 de " + palo
  
    def identify_card(self, camera):
        '''
        Identifies which card is going to be inserted, or which card was played.

        Parameters
        ----------
        camera : int
            The camera that aims to the card to be identified.

        Returns
        -------
        card : string
            The identified card.
        '''
        card_image = None

        # Take pictures until a card is found
        while card_image is None:

            self.pi_raw_capture.truncate(0)
            #print("truncado")

            # Capture an image with the card
            image = self.capture_image(camera)
            #print("captura de la imagen")

            # Find the card in the image
            card_image = self.prueba(image)
            #print("Prueba")

        # Extract the card's features
        #card_features = self.extract_card_features(card_image)
        #print("caracteristicas")

        # Determine the card based on the isolated features
        #card = self.determine_card(card_features)
        #print("carta")

        # Return the identified card
        return card_image
 
