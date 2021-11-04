/*
  Lora Send And Receive
  This sketch demonstrates how to send and receive data with the MKR WAN 1300/1310 LoRa module.
  This example code is in the public domain.
*/

#include <MKRWAN.h>
#include "DHT.h"
#define DHTPIN 2  
#define DHTTYPE DHT22
#define LightSensor A1

LoRaModem modem;

// Uncomment if using the Murata chip as a module
// LoRaModem modem(Serial1);

#include "arduino_secrets.h"
// Please enter your sensitive data in the Secret tab or arduino_secrets.h
String appEui = SECRET_APP_EUI;
String appKey = SECRET_APP_KEY;
DHT dht(DHTPIN, DHTTYPE);
void setup() {
  // put your setup code here, to run once:
  pinMode(LightSensor, OUTPUT);
  //Serial.begin(115200);

  
  
  dht.begin();
  
  // change this to your regional band (eg. US915, AS923, ...)
  if (!modem.begin(EU868)) {
    Serial.println("Failed to start module");
    while (1) {}
  };
  Serial.print("Your module version is: ");
  Serial.println(modem.version());
  Serial.print("Your device EUI is: ");
  Serial.println(modem.deviceEUI());

  int connected = modem.joinOTAA(appEui, appKey);
  if (!connected) {
    Serial.println("Something went wrong; are you indoor? Move near a window and retry");
    while (1) {}
  }

  // Set poll interval to 60 secs.
  modem.minPollInterval(60);
  // NOTE: independent of this setting, the modem will
  // not allow sending more than one message every 2 minutes,
  // this is enforced by firmware and can not be changed.
}

void loop() {
  Serial.println();
  Serial.println("Enter a message to send to network");
  Serial.println("(make sure that end-of-line 'NL' is enabled)");

  int val = analogRead(LightSensor);
  //Serial.println(val);
  String category = "";
    if (val < 20){
        category = "pitch black";
    }
    else if (val < 50){
        category = "very dark";
    }
    else if (val < 150){
        category = "dark";
    }
    else if (val < 250){
        category = "dim";
    }
    else if (val < 500){
        category = "bright";
    }
    else if (val > 500){
        category = "very bright";
    }
    else {
      Serial.println("Error");
    }
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  String values = (String) t+","+(String) h+","+(String) category;
  Serial.println(values);
  
  int err;
  modem.beginPacket();
  modem.print(values);
  err = modem.endPacket(true);
  if (err > 0) {
    Serial.println("Message sent correctly!");
  } else {
    Serial.println("Error sending message :(");
    Serial.println("(you may send a limited amount of messages per minute, depending on the signal strength");
    Serial.println("it may vary from 1 message every couple of seconds to 1 message every minute)");
  }
  delay(60000);
  if (!modem.available()) {
    Serial.println("No downlink message received at this time.");
    return;
  }
  char rcv[64];
  int i = 0;
  while (modem.available()) {
    rcv[i++] = (char)modem.read();
  }
  Serial.print("Received: ");
  for (unsigned int j = 0; j < i; j++) {
    Serial.print(rcv[j] >> 4, HEX);
    Serial.print(rcv[j] & 0xF, HEX);
    Serial.print(" ");
  }
  Serial.println();
}
