#include <FreeSixIMU.h>
#include <FIMU_ADXL345.h>
#include <FIMU_ITG3200.h>
#include <Wire.h>

#include "CommunicationUtils.h"

#define TCAADDR 0x70

extern "C" { 
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}

extern volatile unsigned long timer0_millis;

float vals[12];
uint32_t time;
uint32_t time_send;
static uint32_t lWaitMillis;

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
  noInterrupts ();
  timer0_millis = 0;
  interrupts ();
  
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
  
  lWaitMillis = millis()+6;
  time_send = 0;
  
}



void loop(){
  time = millis();
  if( (long)(millis() - lWaitMillis ) >= 0) {
    tcaselect(2);
    my3IMU.getValues(vals);
    tcaselect(3);
    my3IMU.getValues(&vals[6]);
    Serial.print("PS");
    Serial.write((uint8_t* )vals, sizeof(vals));
    Serial.write((uint8_t* )&time, sizeof(time));
    Serial.flush();
    lWaitMillis+=6;
    time_send+=abs((long)(time - lWaitMillis));

  }
}

