#include <Servo.h>
const int PWMA = 6;    // Pin PWM para controlar la velocidad del motor
const int AIN1 = 5;    // Pin para controlar la dirección del motor
const int AIN2 = 3;    // Pin para controlar la dirección del motor
const int STBY = 7;    // Pin para activar/desactivar el controlador
int encoderPin = 2;    // Pin para recibir la salida del encoder
int encoderLastState = 0;  // Ultimo estado leido del encoder
int ejectedCards = 0;
bool automaticMode = false;
Servo myServo;  // Crea un objeto servo para controlar el servo motor 

int place = 0;    // Variable para almacenar la placeición del servo 

void setup() 
{ 
  myServo.attach(12);  // Conecta el servo motor al pin 7
  pinMode(PWMA, OUTPUT);
  pinMode(AIN1, OUTPUT);
  pinMode(AIN2, OUTPUT);
  pinMode(STBY, OUTPUT);
  pinMode(encoderPin, INPUT);  // Configuración del pin conectado al encoder como entrada 
  digitalWrite(STBY, HIGH); // Activar el controlador de motor
  Serial.begin(9600);  // Inicializar la comunicación serial para imprimir resultados

  //Motor siempre encendido
  digitalWrite(AIN1, HIGH);
  digitalWrite(AIN2, LOW);
  analogWrite(PWMA, 255);
} 

void loop() 
{
  if (!automaticMode) {
  
    int orderReceived = false;
      // Esperar a recibir el carácter 'p' por el monitor serial
    while (true){
      if (Serial.available() > 0) {
        char incomingByte = Serial.read(); // Lee el dato entrante
        if (incomingByte == 'p'){
          break;
        }
      }
    }
  }
  
  // Hace que el servo vaya de 0 grados a 180 grados en 1 segundo
  for (place = 2; place <= 180; place += 1) { 
    myServo.write(place);              
    delay(1000/180);                       
  }

  // Hace que el servo vaya de 180 grados a 0 grados en 1 segundo
  for (place = 178; place >= 0; place -= 1) { 
    myServo.write(place);              
    delay(1000/180);                       
  }
  
  for (int i = 0; i < 500; i++) {
    //Obtención del estado actual del encoder
    int encoderActualState = digitalRead(encoderPin);
    
    // Comprobar si el pin está en estado alto (encendido)
    if (encoderActualState == LOW && encoderLastState == HIGH) {
      ejectedCards += 1;
      Serial.print("Cartas expulsadas = ");
      Serial.println(ejectedCards);
      break;
    }

    //Se actualiza el ultimo cambio del encoder
    encoderLastState = encoderActualState;
    delay(10);
  }

   delay(1000);
} 
