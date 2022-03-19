#include <Servo.h> // Incluye la carpeta que tiene los controladores de los motores sin escobillas.
Servo esc1; // Define el motor 01 con esc1
Servo esc2; // Define el motor 02 con esc2
int b; // Define una variable entera b que sirve para entregar los valores del sensor.
int a; // Define una variable entera a que sirve para determinar la velocidad de los motores. 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600); // Velocidad de la comunicación serial
  Serial.println("Hello Python"); // Parámetro de entrada que establece la comunicación con python
  esc1.attach(9); // Identifica la salida que se comunica con el motor 01 
  esc2.attach(8); // Identifica la salida que se comunica con el motor 02
  esc1.write(0);  // Define la velocidad inicial del motor 01 a "cero"
  esc2.write(0);  // Define la velocidad inicial del motor 02 a "cero"
  delay(5000);    // Espera cinco segundos para que el controlador de los motores inicie
  esc1.write(10); // Coloca al motor 01 en espera
  esc2.write(10); // Coloca al motor 02 en espera
}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial.available()){ // Mientras el puerto serial reciba haga...
     a = Serial.parseInt(); // Convierte la señal del puerto serial en un entero
     if (a == 0){           // Si el entero es igual a "cero" haga... el espacio es vacio porque arduino espera a que los motores inicien
     }
     else if(a==10)  // Si el entero es igual a 10... coloque los motores en modo de espera
     {
       esc1.write(10);
       esc2.write(10); 
     }
     else          // Sino defina la velicidad de los motores a "a"
     {
     esc1.write(a);
     esc2.write(a); 
     }
     b = analogRead(0); // Lea la señal del sensor y guardela en b
     Serial.println(b); // Envíe la señal del sensor a Python
  }
}
