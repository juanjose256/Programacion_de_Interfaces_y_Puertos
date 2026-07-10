#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <DHT.h>

// Configuración de pines
#define DHTPIN 4
#define DHTTYPE DHT11

Adafruit_BMP280 bmp; // Conexión I2C (SDA a A4, SCL a A5 en Arduino Uno)
DHT dht(DHTPIN, DHTTYPE);

unsigned long contador = 1;
bool bmp_ok = false;

void setup() {
  // Inicialización del puerto serial a 115200 baudios
  Serial.begin(115200);
  while (!Serial); // Esperar a que el puerto serial esté listo
  
  Serial.println(F("# Iniciando lectura de sensores..."));

  // Inicializar DHT11
  dht.begin();

  // Intentar iniciar el BMP280 en la dirección común 0x76
  if (bmp.begin(0x76)) {
    bmp_ok = true;
    Serial.println(F("# BMP280 OK (0x76)"));
  } else {
    // Si no responde en 0x76, intentar en 0x77
    if (bmp.begin(0x77)) {
      bmp_ok = true;
      Serial.println(F("# BMP280 OK (0x77)"));
    } else {
      // Mensaje de advertencia, pero NO congelamos el Arduino con un while(1)
      Serial.println(F("# Advertencia: Sensor BMP280 no detectado. Revisa las conexiones I2C."));
    }
  }
  
  Serial.println(F("# Configuración completa. Iniciando transmisión de datos en formato CSV..."));
}

void loop() {
  // El DHT11 requiere al menos 2 segundos entre lecturas
  delay(2000);

  float temp = 0.0;
  float pres = 0.0;
  float alt = 0.0;
  float hum = 0.0;

  // 1. Leer humedad del DHT11
  hum = dht.readHumidity();
  if (isnan(hum)) {
    hum = 0.0; // Fallback si la lectura falla
  }

  // 2. Leer temperatura, presión y altitud
  if (bmp_ok) {
    temp = bmp.readTemperature();
    pres = bmp.readPressure() / 100.0; // Convertir Pascals a hectopascales (hPa)
    alt = bmp.readAltitude(1013.25);   // Altitud estimada con presión al nivel del mar de 1013.25 hPa
  } else {
    // Si el BMP280 falló, intentamos leer la temperatura del DHT11 como respaldo
    temp = dht.readTemperature();
    if (isnan(temp)) {
      temp = 0.0;
    }
    pres = 0.0;
    alt = 0.0;
  }

  // 3. Imprimir datos en formato CSV: N,temp,pres,hum,alt
  // Las líneas que comienzan con '#' son tratadas como comentarios por LAB7.py
  Serial.print(contador);
  Serial.print(",");
  Serial.print(temp, 2);
  Serial.print(",");
  Serial.print(pres, 2);
  Serial.print(",");
  Serial.print(hum, 2);
  Serial.print(",");
  Serial.println(alt, 2);

  contador++;
}