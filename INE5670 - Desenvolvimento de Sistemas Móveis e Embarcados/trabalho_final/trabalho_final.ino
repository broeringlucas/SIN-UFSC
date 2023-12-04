#include "Arduino.h"
#include "DHT.h"
#include "LED.h"
#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Arduino_JSON.h>
#include <string>

#define DHT_PIN D6
#define DHTTYPE DHT11
#define LED_PIN1 D5
#define LED_PIN2 D7

LED ledVermelho(LED_PIN1);
LED ledVerde(LED_PIN2);

DHT dht(DHT_PIN, DHTTYPE);

WiFiClient client;
HTTPClient http;

float tempLimit = 0;

void setup() {
  Serial.begin(9600);
  dht.begin();

  WiFi.begin("", "");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); 
    Serial.println(".");
  }
  Serial.println("");
  Serial.println("Connected to Wifi with IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  float temperature = dht.readTemperature();
  newLimite();

  Serial.print("Limit: ");
  Serial.println(tempLimit);
  Serial.println("");

  if (isnan(temperature)) {
    Serial.println(F("O sensor nao conseguiu ler a temperatura!"));
    return;
  } else {
    Serial.print("Temperatura: ");
    Serial.print(temperature);
    Serial.println("  °C");
  }

  if (tempLimit != 0) {
    if (temperature >= tempLimit) {
      ledVermelho.on();
      ledVerde.off();
      Serial.println("LED VERMELHO ACESO!!");
      Serial.println("");
    } else {
      ledVerde.on();
      ledVermelho.off();
      Serial.println("LED VERDE ACESO!!");
      Serial.println("");
    }
  }

  while (Serial.available()) {
    Serial.read();
  }

  postTemp(temperature);

  delay(10000);
}


void newLimite() {
  if (WiFi.status() == WL_CONNECTED) {
    http.begin(client, "http://192.168.0.173:3000/config");
    int httpCode = http.GET();
    String payload = http.getString();

    Serial.print("GET STATUS: ");
    Serial.println(httpCode);

    Serial.print("GET PAYLOAD:");
    Serial.println(payload);
    Serial.println("");

    JSONVar myObject = JSON.parse(payload);

    if (JSON.typeof(myObject) == "undefined") {
      Serial.println("Parsing failed");
      return;
    }
    
    double limit = (myObject["tempLimit"]);
    tempLimit = limit;
    http.end();
  } else {
    Serial.println("Error in Wifi connection");
  }
}

void postTemp(float temperature) {
  if (WiFi.status() == WL_CONNECTED) {
    String jsonPayload = "{\"temp\":" + String(temperature) + "}";
    http.begin(client, "http://192.168.0.173:3000/logs");
    http.addHeader("Content-type", "application/json");
    int httpCode = http.POST(jsonPayload);
    String payload = http.getString();

    Serial.print("POST STATUS: ");
    Serial.println(httpCode);

    Serial.print("POST PAYLOAD: ");
    Serial.println(payload);
    Serial.println("");

    http.end();
    delay(2000);
  } else {
    Serial.println("Error in Wifi connection");
  }
}
