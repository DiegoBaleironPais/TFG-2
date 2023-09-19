import tensorflow as tf

# Cargar tu modelo .h5
model = tf.keras.models.load_model('./ModeloEntrenado/number_preditor.h5')

# Convertir el modelo a formato TF Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Guardar el modelo convertido
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
    print("Conversion Correcta")
