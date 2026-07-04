// LAB 4 - BMP280 (I2C) + OLED SSD1306 (SPI) + RTC DS1307 (I2C)
// Incluye Actividades de Analisis 1, 2 y 3
// NOTA: todos los textos usan F() para vivir en Flash y no agotar los 2KB de RAM del Uno
#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <RTClib.h>

#define OLED_CS   10
#define OLED_DC   9
#define OLED_RST  8

#define LED_ALARMA        7
#define TEMP_UMBRAL_ON    35.0
#define TEMP_UMBRAL_OFF   33.0

Adafruit_BMP280 bmp;
Adafruit_SSD1306 oled(128, 64, &SPI, OLED_DC, OLED_RST, OLED_CS);
RTC_DS1307 rtc;

bool alarmaActiva = false;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println(F("Iniciando..."));

  pinMode(LED_ALARMA, OUTPUT);
  digitalWrite(LED_ALARMA, LOW);

  Wire.begin();

  // --- Actividad 2: subir velocidad del bus I2C a 400 kHz ---
  Wire.setClock(400000);
  Serial.println(F("Bus I2C configurado a 400 kHz"));

  // --- OLED primero: si falla, no hay memoria/pantalla para mostrar el error, solo Serial ---
  if (!oled.begin(SSD1306_SWITCHCAPVCC)) {
    Serial.println(F("OLED no encontrado!"));
    while (1);
  }
  Serial.println(F("OLED OK"));
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  oled.println(F("OLED OK"));
  oled.display();
  delay(300);

  // --- BMP280 ---
  if (!bmp.begin(0x76)) {
    Serial.println(F("BMP280 no encontrado!"));
    oled.clearDisplay();
    oled.setCursor(0, 0);
    oled.println(F("ERROR: BMP280"));
    oled.println(F("no encontrado!"));
    oled.display();
    while (1);
  }
  Serial.println(F("BMP280 OK (0x76)"));

  bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,
                  Adafruit_BMP280::SAMPLING_X2,
                  Adafruit_BMP280::SAMPLING_X16,
                  Adafruit_BMP280::FILTER_X16,
                  Adafruit_BMP280::STANDBY_MS_500);

  // --- Actividad 1: RTC DS1307 en el mismo bus I2C ---
  if (!rtc.begin()) {
    Serial.println(F("RTC DS1307 no encontrado!"));
    oled.clearDisplay();
    oled.setCursor(0, 0);
    oled.println(F("ERROR: RTC"));
    oled.println(F("no encontrado!"));
    oled.display();
    while (1);
  }
  Serial.println(F("RTC DS1307 OK (0x68)"));

  if (!rtc.isrunning()) {
    Serial.println(F("RTC sin hora, ajustando..."));
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  Serial.println(F("Ambos I2C coexisten sin conflicto."));

  oled.clearDisplay();
  oled.setCursor(0, 0);
  oled.println(F("Sensores listos!"));
  oled.display();
  delay(1000);
}

void loop() {
  // --- Actividad 2: medir tiempo de lectura I2C con micros() ---
  unsigned long t_inicio = micros();
  float t = bmp.readTemperature();
  float p = bmp.readPressure() / 100.0;
  DateTime now = rtc.now();
  unsigned long t_fin = micros();
  unsigned long duracion = t_fin - t_inicio;

  // --- Actividad 3: alarma con histeresis (35 ON / 33 OFF) ---
  if (!alarmaActiva && t >= TEMP_UMBRAL_ON) {
    alarmaActiva = true;
  } else if (alarmaActiva && t <= TEMP_UMBRAL_OFF) {
    alarmaActiva = false;
  }
  digitalWrite(LED_ALARMA, alarmaActiva ? HIGH : LOW);

  // --- Serial ---
  Serial.print(now.year()); Serial.print('/');
  Serial.print(now.month()); Serial.print('/');
  Serial.print(now.day()); Serial.print(' ');
  Serial.print(now.hour()); Serial.print(':');
  Serial.print(now.minute()); Serial.print(':');
  Serial.println(now.second());

  Serial.print(F("Temp: ")); Serial.print(t); Serial.println(F(" C"));
  Serial.print(F("Presion: ")); Serial.print(p); Serial.println(F(" hPa"));
  Serial.print(F("Tiempo lectura I2C: "));
  Serial.print(duracion);
  Serial.println(F(" us"));
  Serial.print(F("Alarma: "));
  Serial.println(alarmaActiva ? F("ACTIVA") : F("apagada"));
  Serial.println(F("---"));

  // --- OLED ---
  oled.clearDisplay();
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  oled.print(now.hour());
  oled.print(':');
  if (now.minute() < 10) oled.print('0');
  oled.print(now.minute());
  oled.print(':');
  if (now.second() < 10) oled.print('0');
  oled.println(now.second());

  oled.setCursor(0, 16);
  oled.print(F("Temp: "));
  oled.print(t, 1);
  oled.println(F(" C"));

  oled.setCursor(0, 32);
  oled.print(F("Presion: "));
  oled.print(p, 1);
  oled.println(F(" hPa"));

  oled.setCursor(0, 48);
  oled.print(alarmaActiva ? F("ALARMA! >35C") : F("Normal"));

  oled.display();

  delay(500);
}