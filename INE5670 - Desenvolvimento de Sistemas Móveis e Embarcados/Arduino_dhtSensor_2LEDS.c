#include "Arduino.h"
#include "DHT.h"
#include "LED.h"

#define DHT_PIN D6
#define DHTTYPE DHT11
#define LED_PIN1 D5
#define LED_PIN2 D7

LED ledVermelho(LED_PIN1);
LED ledVerde(LED_PIN2);

DHT dht(DHT_PIN, DHTTYPE);

float limiteTemp = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();

  delay(2000);

  Serial.println("Menu");
  Serial.println("1 - Escolher Limite Temperatura");
  Serial.println("2 - Sair");


}

void loop() {

  float temperature = dht.readTemperature();

  if (isnan(temperature)) {
    Serial.println(F("O sensor nao conseguiu ler a temperatura!"));
    return;
  } else {
    Serial.print("Temperatura: ");
    Serial.print(temperature);
    Serial.println("  °C");
  }
  if (limiteTemp != 0) {
      if (temperature >= limiteTemp) {
        ledVermelho.on();
        ledVerde.off();
        Serial.println("LED VERMELHO ACESO!!");
    } else {
        ledVerde.on();
        ledVermelho.off();
        Serial.println("LED VERDE ACESO!!");
    }

  }
  if (Serial.available()) {
    int opcao = Serial.parseInt();

    while (Serial.read() != '\n');

    switch (opcao) {
      case 1:
        escolherLimiteTemp();
        break;
      case 2: 
        break;
      default:
        break;
        }
    }

    while (Serial.available()) {
      Serial.read();
    }

  delay(2000);
}

float escolherLimiteTemp() {
    float temperature = dht.readTemperature();

    Serial.println("Digite o novo limite de temperatura:");
    while (Serial.available() == 0);
    limiteTemp = Serial.parseFloat();
    Serial.print("Novo limite de temperatura é: ");
    Serial.println(limiteTemp);

    return limiteTemp;
};