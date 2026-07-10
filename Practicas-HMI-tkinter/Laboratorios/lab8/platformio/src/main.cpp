/**
 * @file main.cpp
 * @brief Código para el microcontrolador (Arduino Uno) para el LAB8 de PlatformIO.
 * 
 * Este código realiza lo siguiente:
 * 1. Secuencia de prueba de hardware al inicio (Rojo -> Verde -> Azul, 500 ms cada uno).
 * 2. Envío periódico de telemetría simulada (falsa) en formato CSV cada segundo (N,temp,pres,hum,alt).
 * 3. Lectura y parseo de comandos seriales:
 */

#include <Arduino.h>

// --- CONFIGURACIÓN DE PINES DEL LED RGB ---
const int PIN_GREEN = 9;   // LED 0 (Verde)
const int PIN_RED = 10;    // LED 1 (Rojo)
const int PIN_BLUE = 11;   // LED 2 (Azul)

// --- CONFIGURACIÓN DEL TIPO DE LED ---
// true para Cátodo Común (GND común), false para Ánodo Común (5V común)
const bool IS_COMMON_CATHODE = true;

// Variables de control de tiempo y datos
unsigned long ultimoEnvio = 0;
const unsigned long INTERVALO_ENVIO = 1000; // 1 segundo
unsigned long contadorDatos = 0;

// Variables simuladas para los sensores
float temperatura = 24.5;
float presion = 1013.25;
float humedad = 50.0;
float altitud = 120.0;

// Declaración de funciones
void apagarLeds();
void setLed(int ledIndex, int state);
void procesarSerial();
void enviarTelemetria();

void setup() {
  Serial.begin(115200);
  
  // Configurar pines como salidas
  pinMode(PIN_RED, OUTPUT);
  pinMode(PIN_GREEN, OUTPUT);
  pinMode(PIN_BLUE, OUTPUT);
  
  // --- SECUENCIA DE PRUEBA DE INICIO (Hardware Test) ---
  // Enciende Rojo -> Verde -> Azul durante 500 ms cada uno
  if (IS_COMMON_CATHODE) {
    digitalWrite(PIN_RED, HIGH); delay(500); digitalWrite(PIN_RED, LOW);
    digitalWrite(PIN_GREEN, HIGH); delay(500); digitalWrite(PIN_GREEN, LOW);
    digitalWrite(PIN_BLUE, HIGH); delay(500); digitalWrite(PIN_BLUE, LOW);
  } else {
    digitalWrite(PIN_RED, LOW); delay(500); digitalWrite(PIN_RED, HIGH);
    digitalWrite(PIN_GREEN, LOW); delay(500); digitalWrite(PIN_GREEN, HIGH);
    digitalWrite(PIN_BLUE, LOW); delay(500); digitalWrite(PIN_BLUE, HIGH);
  }
  
  apagarLeds();
  Serial.println("# MCU listo e inicializado.");
}

void loop() {
  procesarSerial();
  
  unsigned long tiempoActual = millis();
  if (tiempoActual - ultimoEnvio >= INTERVALO_ENVIO) {
    ultimoEnvio = tiempoActual;
    enviarTelemetria();
  }
}

void apagarLeds() {
  if (IS_COMMON_CATHODE) {
    digitalWrite(PIN_RED, LOW);
    digitalWrite(PIN_GREEN, LOW);
    digitalWrite(PIN_BLUE, LOW);
  } else {
    digitalWrite(PIN_RED, HIGH);
    digitalWrite(PIN_GREEN, HIGH);
    digitalWrite(PIN_BLUE, HIGH);
  }
}

void setLed(int ledIndex, int state) {
  int pin = -1;
  if (ledIndex == 0) pin = PIN_GREEN;
  else if (ledIndex == 1) pin = PIN_RED;
  else if (ledIndex == 2) pin = PIN_BLUE;
  
  if (pin != -1) {
    bool valorEscritura;
    if (IS_COMMON_CATHODE) {
      valorEscritura = (state == 1) ? HIGH : LOW;
    } else {
      valorEscritura = (state == 1) ? LOW : HIGH;
    }
    digitalWrite(pin, valorEscritura);
  }
}

void procesarSerial() {
  if (Serial.available() > 0) {
    String entrada = Serial.readStringUntil('\n');
    entrada.trim();
    
    if (entrada.length() == 0) return;
    
    if (entrada.equalsIgnoreCase("PING")) {
      Serial.println("# PONG");
      return;
    }
    
    if (entrada.startsWith("SET:LED:")) {
      int segundoDosPuntos = 7; // Posición de ':' después de "SET:LED"
      int tercerDosPuntos = entrada.indexOf(':', segundoDosPuntos + 1);
      
      if (tercerDosPuntos != -1) {
        String strIndex = entrada.substring(segundoDosPuntos + 1, tercerDosPuntos);
        String strState = entrada.substring(tercerDosPuntos + 1);
        
        int ledIndex = strIndex.toInt();
        int ledState = strState.toInt();
        
        setLed(ledIndex, ledState);
        
        Serial.print("# LED ");
        Serial.print(ledIndex);
        Serial.print(" configurado en ");
        Serial.println(ledState);
      }
    }
  }
}

void enviarTelemetria() {
  contadorDatos++;
  
  // Fluctuaciones simuladas para los datos de los sensores
  temperatura += random(-5, 6) * 0.1;
  presion += random(-2, 3) * 0.05;
  humedad += random(-10, 11) * 0.2;
  altitud += random(-1, 2) * 0.1;
  
  temperatura = constrain(temperatura, 15.0, 45.0);
  presion = constrain(presion, 950.0, 1050.0);
  humedad = constrain(humedad, 20.0, 95.0);
  
  Serial.print(contadorDatos);
  Serial.print(",");
  Serial.print(temperatura, 2);
  Serial.print(",");
  Serial.print(presion, 2);
  Serial.print(",");
  Serial.print(humedad, 2);
  Serial.print(",");
  Serial.println(altitud, 2);
}