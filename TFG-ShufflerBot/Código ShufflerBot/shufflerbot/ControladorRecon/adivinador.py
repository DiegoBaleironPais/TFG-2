import cv2
import matplotlib.pyplot as plt
import numpy as np
import pytesseract

# Número de segmentos para cada palo
segmentos_oros = 2
segmentos_bastos = 5
segmentos_espadas = 3
segmentos_copas = 2

# Porcentaje de color negro en la imagen para cada palo
porcentaje_oros = 83
porcentaje_bastos = 41
porcentaje_espadas = 53.2
porcentaje_copas = 55.66

# Función para recortar una imagen a un área de interés específica
def recortar_imagen(img, inicio_x, inicio_y, fin_x, fin_y):
    # Recorta y devuelve la imagen en el rango especificado
    imagen_recortada = img[inicio_y:fin_y, inicio_x:fin_x]
    return imagen_recortada

def encontrar_y_dibujar_lineas_horizontales_superiores(ruta_imagen, umbral_y=5, umbral=4, longitud_min_linea=3, maxima_distancia_linea=10, limite_altura=15):
    coordenadas_lineas_locales = []
    y_superior = float('inf')
    y_maximo = 0

    # Cargar la imagen desde una ruta de archivo y recortarla
    img = cv2.imread(ruta_imagen, cv2.IMREAD_COLOR)
    imagen_recortada = recortar_imagen(img, 20, 200, 550, 300)
    cv2.imwrite('recorte.jpg', imagen_recortada)

    # Convertir la imagen a escala de grises y aplicar desenfoque
    gris = cv2.cvtColor(imagen_recortada, cv2.COLOR_BGR2GRAY)
    desenfoque = cv2.GaussianBlur(gris, (5, 5), 0)

    # Binarizar la imagen para destacar las características
    _, binarizada = cv2.threshold(desenfoque, 80, 255, cv2.THRESH_BINARY)
    cv2.imwrite('recorteOtsu.jpg', binarizada)

    # Detección de bordes y líneas
    bordes = cv2.Canny(binarizada, 50, 150, apertureSize=7)
    lineas = cv2.HoughLinesP(bordes, 1, np.pi / 180, umbral, longitud_min_linea, maxima_distancia_linea)
    imagen_lineas = np.zeros_like(imagen_recortada)

    # Dibujar las líneas detectadas y almacenar sus coordenadas
    if lineas is not None:
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]
            if abs(y2 - y1) <= umbral_y:
                y_min_linea = min(y1, y2)
                y_max_linea = max(y1, y2)
                # Actualizar y_superior y y_maximo
                y_superior = min(y_superior, y_min_linea)
                # Dibujar la línea si está dentro del rango de limite_altura
                if y_min_linea <= y_superior + limite_altura:
                    y_maximo = max(y_maximo, y_max_linea)
                    cv2.line(imagen_lineas, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    coordenadas_lineas_locales.append((min(x1, x2), max(x1, x2)))

    # Combinar la imagen recortada con las líneas dibujadas
    imagen_combinada = cv2.addWeighted(imagen_recortada, 0.8, imagen_lineas, 1, 0)
    cv2.imwrite('lineaDetectada.jpg', imagen_combinada)
    return binarizada, imagen_combinada, imagen_lineas, coordenadas_lineas_locales, y_superior, y_maximo
    
    
    # Función para añadir líneas rojas en la imagen.
def agregar_lineas_rojas(imagen_combinada, coordenadas_lineas, binarizada, y_superior, y_maximo):
    altura, anchura = imagen_combinada.shape[:2]
    x_esquina_izquierda = 0
    y_esquina_izquierda = y_superior + 12
    y_maximo = y_superior + 12
    segmento_avistado = 0
    numero_segmentos = 0
    contador_pixeles_rojos = 0

    # Pintar líneas rojas donde se detectaron líneas verdes.
    for x1, x2 in coordenadas_lineas:
        imagen_combinada[5, x1:x2] = [0, 0, 255]  # Color rojo en BGR
    
    for x in range(anchura):
        if not np.array_equal(imagen_combinada[5, x], [0, 0, 255]):
            for y in range(y_superior, y_maximo + 1):
                if binarizada[y, x] == 0:
                    imagen_combinada[5, x] = [0, 0, 255]
                    break

    fila_objetivo = 5  # La fila en la que estamos buscando segmentos rojos

    # Iterar a través de cada píxel en la fila específica
    ultimo_pixel_rojo = -1  # Última posición de un píxel rojo encontrado
    for x in range(anchura):
        # Verificar si el píxel actual es rojo
        if np.array_equal(imagen_combinada[fila_objetivo, x], [0, 0, 255]):
            if ultimo_pixel_rojo >= 0 and (x - ultimo_pixel_rojo - 1) <= 25:
                # Conectar este segmento rojo con el anterior
                imagen_combinada[fila_objetivo, ultimo_pixel_rojo + 1:x] = [255, 0, 255]
            ultimo_pixel_rojo = x

    for x in range(anchura):
        if not np.array_equal(imagen_combinada[fila_objetivo, x], [0, 0, 255]):
            segmento_avistado = 0
        else:
            contador_pixeles_rojos += 1
            if segmento_avistado == 0:
                segmento_avistado = 1
                numero_segmentos += 1

    for x in range(anchura):
        if x_esquina_izquierda == 0 and np.array_equal(imagen_combinada[fila_objetivo, x], [0, 0, 255]):
            x_esquina_izquierda = x
        if np.array_equal(imagen_combinada[fila_objetivo, x], [0, 0, 255]):
            imagen_combinada[y_esquina_izquierda: y_esquina_izquierda + 20, x] = [0, 0, 255]

    # Calcular el porcentaje de la línea que es roja.
    porcentaje_linea = (contador_pixeles_rojos / anchura) * 100
    
    # Coordenadas de la esquina izquierda
    coordenadas_esquina = (y_esquina_izquierda, x_esquina_izquierda)
    cv2.imwrite('lineaDetectada2.jpg', imagen_combinada)    
    return imagen_combinada, numero_segmentos, porcentaje_linea, coordenadas_esquina

def detectar_palo(numero_segmentos, porcentaje_linea):
    # Análisis inicial basado en el número de segmentos
    if numero_segmentos == segmentos_oros:
        palo_probable = "oros o copas"
    elif numero_segmentos == segmentos_espadas:
        palo_probable = "espadas"
    elif numero_segmentos == segmentos_bastos:
        palo_probable = "bastos"
    else:
        palo_probable = "no reconocido por el número de segmentos"

    # Diccionario para almacenar la diferencia de porcentaje para cada palo
    diferencias_porcentaje = {
        'oros': abs(porcentaje_linea - porcentaje_oros),
        'bastos': abs(porcentaje_linea - porcentaje_bastos),
        'espadas': abs(porcentaje_linea - porcentaje_espadas),
        'copas': abs(porcentaje_linea - porcentaje_copas)
    }

    # Encontrar el palo con la diferencia de porcentaje más pequeña
    palo_menor_diferencia = min(diferencias_porcentaje, key=diferencias_porcentaje.get)

    if palo_probable == "oros o copas":
        if palo_menor_diferencia in ["copas", "oros"]:
            palo_final = palo_menor_diferencia
        else:
            palo_final = palo_probable
    elif palo_probable == "no reconocido por el número de segmentos":
        palo_final = palo_menor_diferencia
    else:
        if palo_menor_diferencia == palo_probable:
            palo_final = palo_probable
        else:
            palo_final = palo_menor_diferencia

    return palo_final
    
def extraer_numero(ruta_imagen, coordenadas_esquina, margen_binarizacion=95):
    # Cargar la imagen y recortarla
    img = cv2.imread(ruta_imagen, cv2.IMREAD_COLOR)
    imagen_recortada = recortar_imagen(img, 20, 200, 550, 300)
    
    y, x = coordenadas_esquina
    inicio_y = y
    inicio_x = x
    fin_y = y + 55
    fin_x = x + 48
    
    numero_recortado = imagen_recortada[inicio_y:fin_y, inicio_x:fin_x]
    cv2.imwrite('recorteNumerico.jpg', numero_recortado)  
    gris = cv2.cvtColor(numero_recortado, cv2.COLOR_BGR2GRAY)
    # Cambiar según el número
    print("margen = ", margen_binarizacion)
    _, umbralizado = cv2.threshold(gris, margen_binarizacion, 255, cv2.THRESH_BINARY)
    cv2.imwrite('recorteNumericoBinarizado.jpg', umbralizado)  

    contornos, _ = cv2.findContours(umbralizado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
   
    # Encontrar el contorno con el área más grande
    area_maxima = 0
    contorno_mayor = None
    for contorno in contornos:
        area = cv2.contourArea(contorno)
        # Generar un color aleatorio
        color = np.random.randint(0, 255, size=3).tolist()
        # Dibujar el contorno actual en 'numero_recortado' con el color generado
        cv2.drawContours(numero_recortado, [contorno], -1, color, 2)
        if area > area_maxima:
            area_maxima = area
            contorno_mayor = contorno
    cv2.imwrite('contornos.jpg', numero_recortado)  

    # Si se encuentra un contorno grande, procesar esa parte de la imagen
    if contorno_mayor is not None:
        # Crear una máscara del mismo tamaño que la imagen umbralizada
        mascara = np.zeros_like(umbralizado)

        # Dibujar el contorno más grande en la máscara con color blanco
        cv2.drawContours(mascara, [contorno_mayor], -1, 255, thickness=cv2.FILLED)
        cv2.drawContours(gris, [contorno_mayor], -1, 255, thickness=cv2.FILLED)

        # Invertir la máscara para tener el contorno en negro y el fondo en blanco
        mascara_invertida = cv2.bitwise_not(mascara)

        # Aplicar la máscara invertida a la imagen umbralizada para blanquear fuera del contorno
        resultado_con_contorno_blanco = cv2.bitwise_or(umbralizado, mascara_invertida)
        cv2.imwrite('recorteAislado.jpg', resultado_con_contorno_blanco)  
        resultado_invertido = cv2.bitwise_not(resultado_con_contorno_blanco)

        # Obtención de contornos de nuevo
        contornos, _ = cv2.findContours(resultado_invertido, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        texto = "1"
        if len(contornos) == 0:
            return None, None
            
        if len(contornos) == 1:
            # Configuración de pytesseract para utilizar solo caracteres numéricos
            config_custom = r'-c tessedit_char_whitelist=01234567 --psm 6'
    
            # Utilizar pytesseract para convertir la imagen en texto
            texto = pytesseract.image_to_string(resultado_con_contorno_blanco, config=config_custom).strip()
            if texto == "" or texto == "0":
                coordenadas_x = []

                for contorno in contornos:
                    # Calcular el momento del contorno
                    M = cv2.moments(contorno)
                    if M["m00"] != 0:
                        # Calcular el centroide
                        cX = int(M["m10"] / M["m00"])
                        coordenadas_x.append((cX, contorno))  # Guardar la coordenada x y el contorno

                # Ordenar los contornos de izquierda a derecha según la coordenada x
                coordenadas_x.sort(key=lambda x: x[0])

                # El contorno más a la derecha en la lista ordenada
                contorno_izquierdo = coordenadas_x[-1][1]
                # Calcular el área del contorno
                area = cv2.contourArea(contorno_izquierdo)
        
                # Calcular el rectángulo delimitador y su área
                x, y, w, h = cv2.boundingRect(contorno_izquierdo)
                area_rectangulo = w * h
                
                cv2.rectangle(resultado_con_contorno_blanco, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
                # Calcular la relación de área
                relacion_area = area / area_rectangulo
                #print("Relación de área ",relacion_area) 
                relacion_aspecto = h / float(w)
                #print(f"Relación altura/ancho: {relacion_aspecto:.2f}")
                if relacion_area > 0.6:
                    texto = "5"
                else:
                    # Imprimir la relación entre la altura y el ancho del rectángulo delimitador
                    relacion_aspecto = h / float(w)
                    if relacion_aspecto <= 2.4:
                        texto = "2"
                        #print(f"Relación altura/ancho: {relacion_aspecto:.2f}")
                    else:
                        texto = "1"
        else:
            #print("Número de contornos: ",len(contornos))
            # Inicializa una lista para almacenar las coordenadas x del centroide de cada contorno
            coordenadas_x = []

            for contorno in contornos:
                # Calcular el momento del contorno
                M = cv2.moments(contorno)
                if M["m00"] != 0:
                    # Calcular el centroide
                    cX = int(M["m10"] / M["m00"])
                    coordenadas_x.append((cX, contorno))  # Guardar la coordenada x y el contorno

            # Ordenar los contornos de izquierda a derecha según la coordenada x
            coordenadas_x.sort(key=lambda x: x[0])

            # El contorno más a la derecha en la lista ordenada
            contorno_izquierdo = coordenadas_x[-1][1]
            
            # Calcular el área del contorno
            area = cv2.contourArea(contorno_izquierdo)
    
            # Calcular el rectángulo delimitador y su área
            x, y, w, h = cv2.boundingRect(contorno_izquierdo)
            area_rectangulo = w * h
            
            cv2.rectangle(resultado_con_contorno_blanco, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
            # Calcular la relación de área
            relacion_area = area / area_rectangulo
            #print("Relación de área ",relacion_area) 
            
            if relacion_area > 0.6:
                texto = texto + "0"
            else:
                # Imprimir la relación entre la altura y el ancho del rectángulo delimitador
                relacion_aspecto = h / float(w)
                if relacion_aspecto <= 2.4:
                    texto = texto + "2"
                    #print(f"Relación altura/ancho: {relacion_aspecto:.2f}")
                else:
                    texto = texto + "1"
        
        return resultado_con_contorno_blanco, texto

    return None  # Devolver None si no se encuentra un contorno adecuado
    
carta_binarizada, carta_combinada, imagen_linea_carta, coordenadas_lineas_carta, top_y, max_y = encontrar_y_dibujar_lineas_horizontales_superiores('./Original.jpg')
carta_combinada, numero_segmentos, porcentaje_linea, coordenadas_esquina = agregar_lineas_rojas(carta_combinada, coordenadas_lineas_carta, carta_binarizada, top_y, max_y)    
palo = detectar_palo(numero_segmentos, porcentaje_linea)
print("El palo es: ",palo)
imagen_numerica, numero = extraer_numero('./Original.jpg', coordenadas_esquina)
_, numero2 = extraer_numero('./Original.jpg', coordenadas_esquina, 75)
_, numero3 = extraer_numero('./Original.jpg', coordenadas_esquina, 105)

lista_prioridades = ["6", "3", "7", "5", "10", "11", "12", "1", "2"]

# Código actualizado de toma de decisiones para considerar la variable adicional 'numero3'
def decidir_y_asignar_tres(numero, numero2, numero3, lista_prioridades):
    # Crear una lista con los números y filtrar los que no están en la lista de prioridades
    numeros = [n for n in [numero, numero2, numero3]  if n in lista_prioridades]
    
    # Si hay al menos un número en la lista de prioridades, encontrar el de mayor prioridad
    if numeros:
        # Ordenar los números por su prioridad y devolver el de mayor prioridad (primero en la lista ordenada)
        return sorted(numeros, key=lambda x: lista_prioridades.index(x))[0]
    
    # Si ninguno de los números está en la lista de prioridades o todos los números son iguales, devolver el 'numero' original
    return numero

# Llamar a la función y obtener el resultado
nuevo_numero = decidir_y_asignar_tres(numero, numero2, numero3, lista_prioridades)

print("Carta detectada", nuevo_numero, "de", palo)

# Títulos para las imágenes
titulos = [
    "Imagen Binarizada", "Imagen de Líneas Horizontales", "Imagen Combinada con Línea Roja",
    "Imagen Numérica"
]

# Lista de imágenes para mostrar
lista_imagenes = [
    carta_binarizada, imagen_linea_carta, carta_combinada, imagen_numerica
]


# Mostrar las imágenes utilizando Matplotlib
def mostrar_imagenes(imagenes, titulos):
    numero_imagenes = len(imagenes)
    numero_columnas = 4
    numero_filas = numero_imagenes // numero_columnas + (numero_imagenes % numero_columnas > 0)

    fig, ejes = plt.subplots(numero_filas, numero_columnas, figsize=(15, 5 * numero_filas))
    for i, ax in enumerate(ejes.flatten()):
        if i < numero_imagenes:  # Solo mostrar las imágenes que tenemos
            if len(imagenes[i].shape) == 2:  # Si la imagen está en escala de grises
                ax.imshow(imagenes[i], cmap='gray')
            else:
                ax.imshow(cv2.cvtColor(imagenes[i], cv2.COLOR_BGR2RGB))
            ax.set_title(titulos[i])
        ax.axis('off')
    plt.tight_layout()
    plt.show()
    
# Llamada a la función para mostrar las imágenes
mostrar_imagenes(lista_imagenes, titulos)
