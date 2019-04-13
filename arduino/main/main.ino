/*

  A program to take vital readings for the plants.

  Example of BH1750 library usage.

  This example initialises the BH1750 object using the default high resolution
  continuous mode and then makes a light level reading every second.

  Connection:

    VCC -> 3V3 or 5V
    GND -> GND
    SCL -> SCL (A5 on Arduino Uno, Leonardo, etc or 21 on Mega and Due, on esp8266 free selectable)
    SDA -> SDA (A4 on Arduino Uno, Leonardo, etc or 20 on Mega and Due, on esp8266 free selectable)
    ADD -> (not connected) or GND

  ADD pin is used to set sensor I2C address. If it has voltage greater or equal to
  0.7VCC voltage (e.g. you've connected it to VCC) the sensor address will be
  0x5C. In other case (if ADD voltage less than 0.7 * VCC) the sensor address will
  be 0x23 (by default).

*/

#include <BH1750.h>
#include <Wire.h>
#include <SoftwareSerial.h>

BH1750 lightMeter;
SoftwareSerial BT(10, 11);

//int sendCounter = 10;

void setup(){

  Serial.begin(9600);

  // Initialize the I2C bus (BH1750 library doesn't do this automatically)
  Wire.begin();
  // On esp8266 you can select SCL and SDA pins using Wire.begin(D4, D3);

  lightMeter.begin();

  Serial.println(F("BH1750 Test begin"));

  BT.begin(9600);
  Serial.println("Bluetooth Initialised");
}


void loop() {

  // Get light readings
  float lux = lightMeter.readLightLevel();
  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");

  // Handle Bluetooth
  Serial.println("Sending BT transmission");
  
  BT.print("$SLux=");
  BT.print(lux);
  BT.println("$E");
//  BT.println(sendCounter);
  
//  sendCounter++;
//  if (sendCounter > 99) sendCounter = 10;
  delay(3721);

}
