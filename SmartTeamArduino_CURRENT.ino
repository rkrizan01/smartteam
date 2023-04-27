#include <SoftwareSerial.h>

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL375.h>

SoftwareSerial BTserial(2, 3); // RX | TX


#define ADXL375_SCK 13
#define ADXL375_MISO 12
#define ADXL375_MOSI 11
#define ADXL375_CS 10


#define FORCE_SENSOR1_PIN0 A0 // FSensor 1
#define FORCE_SENSOR2_PIN1 A1 // FSensor 2
#define FORCE_SENSOR3_PIN2 A2 // FSensor 3
#define FORCE_SENSOR4_PIN3 A3 // FSensor 4
#define FORCE_SENSOR5_PIN4 A5 // FSensor 5


Adafruit_ADXL375 accel = Adafruit_ADXL375(12345);

// setup accelerometer to be read from
void setup() {

  Serial.begin(9600);
  BTserial.begin(9600);

  while (!Serial);
    Serial.println("ADXL375 Accelerometer Test"); Serial.println("");
    if(!accel.begin())
    {
      Serial.println("Ooops, no ADXL375 detected ... Check your wiring!");
      exit(-1);
    }
    // Range: +-200g
}

// Reading data from 5 pins (FSensors)
// Extract the X, Y, and Z accel data from port 9600
// sensor data is printed onto the terminal. Waits 100ms before looping.
void loop() {
  // BTserial.println("MICHAEL GEARY");
  Serial.println("Sent BT message");
 
  sensors_event_t event;
  accel.getEvent(&event);

  int sensorValueX = event.acceleration.x;
  int sensorValueY = event.acceleration.y;
  int sensorValueZ = event.acceleration.z;

  int sensorValue1 = analogRead(FORCE_SENSOR1_PIN0);
  int sensorValue2 = analogRead(FORCE_SENSOR2_PIN1);
  int sensorValue3 = analogRead(FORCE_SENSOR3_PIN2);
  int sensorValue4 = analogRead(FORCE_SENSOR4_PIN3);
  int sensorValue5 = analogRead(FORCE_SENSOR5_PIN4);

  //IMPORTANT: String has to be in Form: 1234,1234,1234,1234;
  //every Value has to be seperated through a comma (',') and the message has to
  //end with a semicolon (';'))

  BTserial.print("{");

  BTserial.print("\"FSensor1\" :");
  BTserial.print(sensorValue1);
  BTserial.print(", ");

  BTserial.print("\"FSensor2\" : ");
  BTserial.print(sensorValue2);
  BTserial.print(", ");

  BTserial.print("\"FSensor3\" : ");
  BTserial.print(sensorValue3);
  BTserial.print(", ");

  BTserial.print("\"FSensor4\" : ");
  BTserial.print(sensorValue4);
  BTserial.print(", ");

  BTserial.print("\"FSensor5\" : ");
  BTserial.print(sensorValue5);
  BTserial.print(", ");

  BTserial.print("\"AccelX\" : ");
  BTserial.print(sensorValueX);
  BTserial.print(", ");

  BTserial.print("\"AccelY\" : ");
  BTserial.print(sensorValueY);
  BTserial.print(", ");

  BTserial.print("\"AccelZ\" : ");
  BTserial.print(sensorValueZ);
  BTserial.println("}");
  delay(1000);
}

