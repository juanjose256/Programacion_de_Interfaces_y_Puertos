#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_BMP280.h>

#define SCREEN_W  128
#define SCREEN_H   64
#define OLED_RST   -1
#define OLED_ADDR  0x3C
#define PIN_LED     4

#define TEMP_LOW   22.8f
#define TEMP_HIGH  24.0f

Adafruit_SSD1306 display(SCREEN_W, SCREEN_H, &Wire, OLED_RST);
Adafruit_BMP280  bmp;
bool ledOn = false;

// ── Intenta iniciar el BMP280 ──
bool iniciarBMP() {
    if (bmp.begin(0x76)) return true;
    if (bmp.begin(0x77)) return true;
    return false;
}

// ── Detecta si la lectura es basura ──
bool lecturaValida(float temp, float pres) {
    if (isnan(temp) || isnan(pres))   return false;
    if (temp < -40  || temp > 85)     return false;  // fuera de rango físico
    if (pres < 300  || pres > 1100)   return false;  // fuera de rango físico
    return true;
}

void setup() {
    Serial.begin(115200);
    delay(1000);
    Wire.begin(21, 22);

    pinMode(PIN_LED, OUTPUT);
    digitalWrite(PIN_LED, LOW);

    if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
        Serial.println("OLED no encontrada");
        while (true);
    }

    if (!iniciarBMP()) {
        Serial.println("BMP280 no encontrado");
        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(SSD1306_WHITE);
        display.setCursor(0, 0);
        display.println("BMP280 ERROR");
        display.println("Revisa cableado");
        display.display();
        while (true);
    }

    Serial.println("Todo OK");
}

void loop() {
    float temp = bmp.readTemperature();
    float pres = bmp.readPressure() / 100.0F;

    // ── Si lectura es basura → reinicia el sensor ──
    if (!lecturaValida(temp, pres)) {
        Serial.println("Lectura invalida, reiniciando BMP280...");

        display.clearDisplay();
        display.setTextColor(SSD1306_WHITE);
        display.setTextSize(1);
        display.setCursor(0, 20);
        display.println("Sensor error...");
        display.println("Reiniciando...");
        display.display();

        delay(500);
        Wire.end();
        delay(200);
        Wire.begin(21, 22);
        delay(200);

        if (!iniciarBMP()) {
            Serial.println("Sensor no responde");
            delay(1000);
            return;
        }
        Serial.println("BMP280 recuperado!");
        return;  // salta este ciclo, siguiente ya será válido
    }

    // ── Histéresis ──
    if (!ledOn && temp > TEMP_HIGH) {
        ledOn = true;
    } else if (ledOn && temp < TEMP_LOW) {
        ledOn = false;
    }
    digitalWrite(PIN_LED, ledOn ? HIGH : LOW);

    // ── Serial ──
    Serial.printf("Temp: %.2f C | Pres: %.1f hPa | LED: %s\n",
                  temp, pres, ledOn ? "ON" : "OFF");

    // ── OLED ──
    display.clearDisplay();
    display.setTextColor(SSD1306_WHITE);

    display.setTextSize(1);
    display.setCursor(0, 0);
    display.println("=== CONTROL TEMP ===");

    display.setTextSize(2);
    char buf[16];
    snprintf(buf, sizeof(buf), "%.2fC", temp);
    display.setCursor(0, 14);
    display.println(buf);

    display.setTextSize(1);
    snprintf(buf, sizeof(buf), "%.1f hPa", pres);
    display.setCursor(0, 38);
    display.println(buf);

    display.setCursor(0, 48);
    display.printf("Rango:%.1f-%.1fC", TEMP_LOW, TEMP_HIGH);

    display.setTextSize(1);
    display.setCursor(0, 58);
    if (ledOn) {
        display.println("CALOR - LED ON ***");
    } else {
        display.println("OK    - LED OFF");
    }

    display.display();
    delay(1000);
}