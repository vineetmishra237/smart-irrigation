#include <Arduino.h>
#include "DHTesp.h"
#include <WiFi.h>
#include <WiFiClient.h>
#include "ThingSpeak.h"
#include <Firebase_ESP_Client.h>
#include <RTClib.h>
#include <Wire.h>
#include <ESP32Servo.h>

#define DHT1_PIN 23
#define DHT2_PIN 22
#define DHT3_PIN 21
#define LDR_PIN 34
#define MQ2_PIN 35
#define TEMP_PIN 34
#define SERVO_PIN 15

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const int myChannelNumber =3036993 ;
const char* myApiKey = "58HDE21EVXSSMPC4";
const char* server = "api.thingspeak.com";

#define DATABASE_URL "https://iotricity-0109-default-rtdb.firebaseio.com/"
#define API_KEY "AIzaSyBM5BdxhxUwYYL223nfFiHPXEUBn9hCZ9Q"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

DHTesp dhtSensor1;
DHTesp dhtSensor2;
DHTesp dhtSensor3;
RTC_DS1307 rtc;
WiFiClient client;

Servo myServo;
bool servoActive = false;
unsigned long servoStartTime = 0;
int servoDuration = 0;

const float GAMMA = 0.7;
const float RL10 = 50;
const float BETA = 3950;// NTC thermistor

int status = WL_IDLE_STATUS;

void setup() {
  Serial.begin(115200);
  myServo.attach(SERVO_PIN);
  myServo.write(0);
  // if (!rtc.begin()) {
  //   Serial.println("Couldn't find RTC");
  //   while (1);
  // }

  dhtSensor1.setup(DHT1_PIN, DHTesp::DHT22);
  dhtSensor2.setup(DHT2_PIN, DHTesp::DHT22);
  dhtSensor3.setup(DHT3_PIN, DHTesp::DHT22);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  Serial.println(WiFi.localIP());
  Serial.println("Connected to WiFi!");

  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("Firebase signUp OK");
  } else {
    Serial.printf("signUp failed: %s\n", config.signer.signupError.message.c_str());
  }
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);

  ThingSpeak.begin(client);
}

void loop() {
  TempAndHumidity data1 = dhtSensor1.getTempAndHumidity();
  TempAndHumidity data2 = dhtSensor2.getTempAndHumidity();
  TempAndHumidity data3 = dhtSensor3.getTempAndHumidity();
  //Serial.println("Temp: " + String(data.temperature, 2) + "°C");
  Serial.println("Humidity: " + String(data1.humidity, 1) + "%");
  Serial.println("Humidity: " + String(data2.humidity, 1) + "%");
  Serial.println("Humidity: " + String(data3.humidity, 1) + "%");
  
  ThingSpeak.setField(1, data1.humidity);
  ThingSpeak.setField(2, data2.humidity);
  ThingSpeak.setField(3, data3.humidity);
  
  
  int x = ThingSpeak.writeFields(myChannelNumber, myApiKey);
  if (x == 200) {
    Serial.println("ThingSpeak push successful");
  } else {
    Serial.println("ThingSpeak push error: " + String(x));
  }

  int ldrValue = analogRead(LDR_PIN);
  float voltage = ldrValue / 1024.0 * 5;
  float resistance = 2000 * voltage / (1 - voltage / 5);
  float lux = pow(RL10 * 1e3 * pow(10, GAMMA) / resistance, (1 / GAMMA));
  
  // --- MQ2 ---
  int gasValue = analogRead(MQ2_PIN);

  // --- Temperature ---
  int tempValue = analogRead(TEMP_PIN);
  float celsius = 1 / (log(1 / (1023. / tempValue - 1)) / BETA + 1.0 / 298.15) - 273.15;

  // --- RTC ---
  // DateTime now = rtc.now();
  // String currentTime = String(now.hour()) + ":" + String(now.minute());


  if (Firebase.RTDB.setFloat(&fbdo, "/sensor/humidity1", data1.humidity)) {
    Serial.println("Firebase: Humidity uploaded");
  } else {
    Serial.println("Firebase error: " + fbdo.errorReason());
  }

  if (Firebase.RTDB.setFloat(&fbdo, "/sensor/humidity2", data1.humidity)) {
    Serial.println("Firebase: Humidity uploaded");
  } else {
    Serial.println("Firebase error: " + fbdo.errorReason());
  }

  if (Firebase.RTDB.setFloat(&fbdo, "/sensor/humidity3", data1.humidity)) {
    Serial.println("Firebase: Humidity uploaded");
  } else {
    Serial.println("Firebase error: " + fbdo.errorReason());
  }

  if (Firebase.RTDB.setFloat(&fbdo, "/sensor/day-light", lux)) {
    Serial.println("Firebase: Ambient Temperature uploaded");
  } else {
    Serial.println("Firebase error: " + fbdo.errorReason());
  }

  if (Firebase.RTDB.setFloat(&fbdo, "/sensor/spoilage", gasValue)) {
    Serial.println("Firebase: Temperature uploaded");
  } else {
    Serial.println("Firebase error: " + fbdo.errorReason());
  }

  if (Firebase.RTDB.setFloat(&fbdo, "/sensor/ambient-temp", celsius)) {
    Serial.println("Firebase: Temperature uploaded");
  } else {
    Serial.println("Firebase error: " + fbdo.errorReason());
  }
  // if (Firebase.RTDB.setString(&fbdo, "/sensor/time", currentTime)) {
  //   Serial.println("Firebase: Time uploaded");
  // } else {
  //   Serial.println("Firebase error: " + fbdo.errorReason());
  // }
  
  // if (Firebase.RTDB.getString(&fbdo, "/control/time")) {
  //   String feedTime = fbdo.stringData();
  //   if (currentTime == feedTime && !servoActive) {
  //     if (Firebase.RTDB.getInt(&fbdo, "/control/pump_runtime_seconds")) {
  //       servoDuration = fbdo.intData();
  //       myServo.write(90);
  //       servoActive = true;
  //       servoStartTime = millis();
  //       Serial.println("Feeding started!");
  //     }
  //   }
  // }

  // --- Stop servo after duration ---
  if (servoActive && millis() - servoStartTime > servoDuration * 1000) {
    myServo.write(0);
    servoActive = false;
    Serial.println("Feeding stopped.");
  }

  Serial.println("---");
  delay(3000);
}