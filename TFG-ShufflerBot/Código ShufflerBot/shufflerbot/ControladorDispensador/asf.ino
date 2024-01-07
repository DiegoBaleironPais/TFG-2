#include <Servo.h>

Servo myServo;             // Crea un objeto servo para controlar el servo motor 

const int PWMA = 6;        // Pin PWM para controlar la velocidad del motor
const int AIN1 = 5;        // Pin para controlar la dirección del motor
const int AIN2 = 3;        // Pin para controlar la dirección del motor
const int STBY = 7;        // Pin para activar/desactivar el controlador
const int pinServo = 12;   // Pin para controlar el servomotor

void setup() 
{ 
  myServo.attach(pinServo);  
  pinMode(PWMA, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(STBY, OUTPUT);
  digitalWrite(STBY, HIGH); // Activar el controlador de motor
  Serial.begin(9600);  // Inicializar la comunicación serial

  //Motor comienza encendido
  digitalWrite(AIN1, LOW);
  digitalWrite(AIN2, HIGH);
  analogWrite(PWMA, 255);
} 

void loop() 
{
   int place = 0; //Variable con la posicion del servo

   while (true) {
        // Esperar para recibir ordenes por el monitor serial
        if (Serial.available() > 0) {
            char siguienteOrden = Serial.read(); // Lee el dato entrante
            switch (siguienteOrden) {
                // Activando rodillos externos
                case 's':
                    analogWrite(PWMA, 255);
                    break; 
                // Apagando rodillos externos
                case 't':
                    analogWrite(PWMA, 0);
                    break;
                // Dispensado siguiente carta
                case 'n':
                    // Colocar la carta en posición
                    for (place = 0; place <= 180; place += 1) { 
                        myServo.write(place);              
                        delay(1000/180);                       
                    }

                    // Expulsar la carta
                    for (place = 180; place >= 0; place -= 1) { 
                        myServo.write(place);              
                        delay(650/180);                       
                    }
            }
        } 
        delay(100);
    }
} 