#include <FreeSixIMU.h>
#include <FIMU_ADXL345.h>
#include <FIMU_ITG3200.h>
#include <Wire.h>

#include "CommunicationUtils.h"
float vals[12];
unsigned long time_start = -1;
unsigned long time;
char flag;


FreeSixIMU my3IMU = FreeSixIMU();
#define TCAADDR 0x70

extern "C" { 
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}


void tcaselect(uint8_t i) {
  if (i > 7) 
  return;
 
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}


void setup() {
  //delay(1000);
  

  /*
  Serial.begin(115200);
  Serial.println("\nTCAScanner ready!");
  
  for (uint8_t t=0; t<8; t++) {
    tcaselect(t);
    Serial.print("TCA Port #"); Serial.println(t);
 
    for (uint8_t addr = 0; addr<=127; addr++) {
      if (addr == TCAADDR) continue;
    
      uint8_t data;
      if (! twi_writeTo(addr, &data, 0, 1, 1)) {
         Serial.print("Found I2C 0x");  Serial.println(addr,HEX);
      }
    }
  }
  Serial.println("\ndone");
  
  Serial.print("DEC");
  */
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
  while(Serial.available()) {
    flag = Serial.read();
    if (flag == 'B')
      time_start = millis();
    if (flag == 'E')
      time_start = -1;
  } 
  
  if (time_start > 0 && !Serial.available()) {
    tcaselect(2);
    my3IMU.getValues(vals);
    tcaselect(3);
    my3IMU.getValues(&vals[6]);
     
    Serial.print("PS"); // Package start
    Serial.flush();
    Serial.write((uint8_t* )vals, sizeof(vals));
    Serial.flush();
    time = millis()-time_start;
    Serial.write((uint8_t* )&time, 4);
    Serial.flush();
  }

}

