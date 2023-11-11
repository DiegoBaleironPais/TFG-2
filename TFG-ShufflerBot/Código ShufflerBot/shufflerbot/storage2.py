
    def insertion_wait(self):
        global photosensor_dispenser
        global inserted_card
        inserted_card = False
        self.controller.enable_digital_reporting(self.photoDispen_pin)
        print("Iniciando espera de insercción.")

        start_time = time.time()  # Guarda el tiempo actual
        try:
            while not inserted_card:
                if time.time() - start_time > 1.5:  # Comprobar si han pasado 3 segundos
                    print("Tiempo de espera excedido. Carta no detectada.")
                    return 1  # Devuelve 1 si la carta no se detecta en 3 segundos
                time.sleep(0.1)  # Pequeña pausa para evitar uso excesivo de CPU
            print("Carta insertada")
            return 0  # Devuelve 0 si la carta es detectada
        except KeyboardInterrupt:
            self.controller.disable_digital_reporting(self.photoDispen_pin)
            print("Espera de insercción interrumpida")
            exit()
        finally:
            self.controller.disable_digital_reporting(self.photoDispen_pin)
