#include <FreeSixIMU.h>
#include <FIMU_ADXL345.h>
#include <FIMU_ITG3200.h>
#include <Wire.h>

#include "CommunicationUtils.h"

#define TCAADDR 0x70
#define STOP 0
#define MEASURE 1
#define UNKNOWN 3

extern "C" { 
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}

float vals[12];
unsigned long time_start = -1;
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

int system_status(){
   while(Serial.available()) {
    flag = Serial.read();
    if (flag == 'B') {
      time_start = millis();
      return MEASURE;
    }
    if (flag == 'E') {
      time_start = -1;
      return STOP;
    }
    return UNKNOWN;
  }
  
  if (time_start > 0)
    return MEASURE;
 
  return STOP;
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

  if (system_status() == MEASURE) {
    tcaselect(2);
    my3IMU.getValues(vals);
    tcaselect(3);
    my3IMU.getValues(&vals[6]);
  }
  if (system_status() == MEASURE) {
    Serial.print("PS"); // Package start
    Serial.flush();
    Serial.write((uint8_t* )vals, sizeof(vals));
    Serial.flush();
  }
  if (system_status() == MEASURE) {
    time = millis()-time_start;
    Serial.write((uint8_t* )&time, 4);
    Serial.flush();
  }
  else {
    time = -1;
    time_start=-1;
    Serial.write((uint8_t* )&time, 4);
    Serial.flush();
  }

}

