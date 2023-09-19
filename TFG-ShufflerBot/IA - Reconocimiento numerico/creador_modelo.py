import os
from tensorflow import keras
from PIL import Image
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, MaxPool2D, Input, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import SGD, Adam
from sklearn.metrics import f1_score, accuracy_score

# Defición de los números a identificar
lista_numeros = [1,2,3,4,5,6,7,10,11,12]

# Ruta a la carpeta que contiene las imágenes
carpeta_imagenes = "C:\\Users\\diego\\Desktop\\Compiladores\\NumerosRecortados"

# Preparación de las listas para guardan las imágenes y las etiquetas
imagenes = []
etiquetas = []

# Leer las imágenes de la carpeta, todas empiezan por Digitos_
for archivo in os.listdir(carpeta_imagenes):
    if archivo.startswith(tuple(map(str, lista_numeros))):  
        # El primer carácter del nombre del archivo es la etiqueta
        etiqueta = int(archivo.split('_')[0])
        #Transformado de las etiquetas para que esten en el rango [1-10], daba problemas de la otra forma  
        etiqueta -= 1
        if (etiqueta > 7):
            etiqueta -= 2

        # Agregación de la etiqueta a la lista de etiquetas
        etiquetas.append(etiqueta)
        
        # Lectura de imagen y ajuste de tamaño
        imagen = Image.open(os.path.join(carpeta_imagenes, archivo))
        imagen = imagen.resize((48, 53))
        
        # Conversión de la imagen a un array numpy y agregación a la lista de imágenes
        imagen = np.array(imagen)
        imagenes.append(imagen)

# Convertir las listas a arrays numpy
imagenes = np.array(imagenes)
etiquetas = np.array(etiquetas)

# Dividisión de los datos en conjuntos de entrenamiento y prueba, actualmente 80% entrenamiento y 20% test
x_train, x_test, y_train, y_test = train_test_split(imagenes, etiquetas, test_size=0.2, random_state=42, stratify=etiquetas)

# Conversión de las etiquetas a categorías one-hot
num_classes = 10
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

# Creación de la arquitectura del modelo
model = Sequential()

model.add(Input(shape=(48, 53, 1)))

model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=(2,2)))

model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=(2,2)))

model.add(Flatten())

model.add(Dense(units=128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=10, activation='softmax'))

# Compilación del modelo
sgd = Adam(learning_rate=0.002)
model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenamiento del modelo
x_train_resh = x_train.reshape((-1, 48, 53, 1))
x_train_resh = x_train_resh/255  # Normalización
x_test_resh = x_test.reshape((-1, 48, 53, 1))
x_test_resh = x_test_resh/255  # Normalización
tf.random.set_seed(1)
model.fit(x_train_resh, y_train, epochs=115, batch_size=4, verbose=1)

# Predicciones
pred = model.predict(x_test_resh)
pred = np.argmax(pred, axis=1)
y_test_single_label = np.argmax(y_test, axis=1)

# Funciones de evaluación
def evaluate_f1(y_true, y_pred):
    f1 = f1_score(y_true, y_pred, average='weighted')
    return f1

def evaluate_acc(y_true, y_pred):
    acc=accuracy_score(y_true, y_pred)
    return acc

# Evaluación del modelo
print('Evaluación F1_score ->',evaluate_f1(y_test_single_label, pred))
print('Evaluación Accuracy ->',evaluate_acc(y_test_single_label, pred))

# Salvado del modelo
model.save('number_preditor.h5')  # Guardar en formato HDF5
model.save('number_preditor')     # Guardar en formato TensorFlow nativo



