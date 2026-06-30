// LAB 2 - PIR KY-017 + OLED SSD1306 en ESP32

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

Adafruit_SSD1306 oled(128,64,&Wire,-1);


volatile bool movimiento = false;
volatile int count = 0;


unsigned long t_actual = 0;
unsigned long t_anterior = 0;


bool mostrando = false;


void IRAM_ATTR isrPIR() {

  movimiento = true;
  count++;

}


void setup(){

  Serial.begin(115200);


  oled.begin(SSD1306_SWITCHCAPVCC,0x3C);
  oled.clearDisplay();
  oled.display();


  pinMode(23, INPUT);


  attachInterrupt(
    digitalPinToInterrupt(23),
    isrPIR,
    RISING
  );

}



void loop(){


  t_actual = millis();



  // Cuando detecta movimiento
  if(movimiento && !mostrando){


    oled.clearDisplay();


    oled.setTextSize(2);
    oled.setTextColor(WHITE);

    oled.setCursor(0,10);
    oled.println("MOVIMIENTO");


    oled.setTextSize(1);
    oled.setCursor(0,40);

    oled.print("Veces: ");
    oled.println(count);


    oled.display();



    Serial.print("[PIR] Movimiento #");
    Serial.println(count);



    // inicia conteo como el delay(2000)
    t_anterior = t_actual;


    mostrando = true;


    movimiento = false;

  }



  // Pasaron 2 segundos -> borrar pantalla
  if(mostrando && (t_actual - t_anterior >= 2000)){


    oled.clearDisplay();
    oled.display();


    mostrando = false;


    t_anterior = t_actual;

  }


}