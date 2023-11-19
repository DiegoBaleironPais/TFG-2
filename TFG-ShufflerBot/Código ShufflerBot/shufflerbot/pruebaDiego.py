import sys
import time
import serial
from telemetrix import telemetrix

from definitions import *
from motor import Motor
from storage import Storage
from card_identifier import CardIdentifier
from gui.robot_app import RobotApp


# - Main program - #

# Initialize the controller
controller = telemetrix.Telemetrix(com_port='/dev/ttyACM0')  # Reemplaza con el puerto correcto
controller.set_pin_mode_digital_output(ENABLE_PIN)
controller.digital_write(ENABLE_PIN, 0)


try:
    # Referencia a la placa arduino del dispensador
    dispenser_serial = serial.Serial('/dev/ttyACM1', 9600)
    print("Dispensador conectado con exito")
except serial.SerialException as e:
    print(f"No se pudo abrir el puerto seriall: {e}")
    sys.exit(1)

# Create the motors
storage_motor = Motor(controller, STORAGE_PULSE_PIN, STORAGE_DIRECTION_PIN, STORAGE_NUM_STEPS, STORAGE_MAX_SPEED, STORAGE_ACCELERATION)
inserter_motor = Motor(controller, INSERTER_PULSE_PIN, INSERTER_DIRECTION_PIN, INSERTER_NUM_STEPS, INSERTER_MAX_SPEED, INSERTER_ACCELERATION)

# Create the card identifier
card_identifier = CardIdentifier(PI_CAM_ID, USB_CAM_ID)


# Start the cameras
card_identifier.start_cam(PI_CAM_ID)
#card_identifier.start_cam(USB_CAM_ID)

# Create the storiage
storage = Storage(controller, storage_motor, inserter_motor, PHOTOSENSOR1_PIN, PHOTOSENSOR2_PIN, DECK, ORDERED_SHUFFLE, EXTRACTOR_STEP, card_identifier)

# Let everything warm up
time.sleep(1)

# Centrado del tabor
storage.reset_position()

# Insertado manual de las cartas
cartas = DECK

storage.insert_next_card("1o", 1, 1)

numCarta = 1
try:
    for carta in cartas:
        leter = input("Inserta la carta {numCarta}: ")
        dispenser_serial.write(b'p')
        if (leter != "p"):
            storage.insert_next_card(carta, numCarta, numCarta)
            numCarta -= 1
        #dispenser_serial.reset_input_buffer()
        numCarta += 1
finally:
    dispenser_serial.close()



#user_input = "" 
#while user_input != "n":
    #Identificar la próxima tarjeta
#    imagen = card_identifier.identify_card(PI_CAM_ID)
#    print("La carta es: ",imagen)
#    user_input = "n"

# for card in DECK:
#    storage.deal_card(card)
#storage.testeo_infrarrojos()
# Stop the cameras
card_identifier.stop_cam(PI_CAM_ID)
#card_identifier.start_cam(USB_CAM_ID)

# Disable the controller
controller.shutdown()
# Close the program
sys.exit(0)
