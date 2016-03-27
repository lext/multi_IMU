#include <FreeSixIMU.h>
#include <FIMU_ADXL345.h>
#include <FIMU_ITG3200.h>
#include <Wire.h>

#include "CommunicationUtils.h"

#define TCAADDR 0x70

extern "C" { 
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}

float vals[12];
unsigned long time;
char flag;



FreeSixIMU my3IMU = FreeSixIMU();


void tcaselect(uint8_t i) {
  if (i > 7) 
  return;
 
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}


void setup() {
  Wire.begin();
  Serial.begin(115200);
  tcaselect(2);
  delay(5);
  my3IMU.init(true);
  delay(5);
  
  tcaselect(3);
  delay(5);
  my3IMU.init(true);
  delay(5);
  
}



void loop(){
        tcaselect(2);
        my3IMU.getValues(vals);
        tcaselect(3);
        my3IMU.getValues(&vals[6]);
        Serial.print("PS"); // Package start
        Serial.write((uint8_t* )vals, sizeof(vals)); // data
        time = millis(); // Time in milliseconds
        Serial.write((uint8_t* )&time, 4);
        Serial.flush();
}

