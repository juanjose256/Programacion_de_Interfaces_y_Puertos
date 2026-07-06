#include <Arduino.h>
// LAB 3 - Arduino: envia temperatura JSON con timestamp, recibe cmd LED
const int PIN_LED = 13;
const int PIN_LM35 = A0;

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED, OUTPUT);
}

void loop() {
  // Leer temperatura
  float v = analogRead(PIN_LM35) * 5.0 / 1023.0;
  float temp = v * 100.0;

  // Enviar JSON con timestamp
  Serial.print("{\"ts\": ");
  Serial.print(millis());
  Serial.print(", \"temp\": ");
  Serial.print(temp, 1);
  Serial.print(", \"led\": ");
  Serial.print(digitalRead(PIN_LED));
  Serial.println("}");

  // Recibir comando
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    if (cmd == "LED_ON")  digitalWrite(PIN_LED, HIGH);
    if (cmd == "LED_OFF") digitalWrite(PIN_LED, LOW);
  }

  delay(500);
}