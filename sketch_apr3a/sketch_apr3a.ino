#include <DallasTemperature.h>.
#include <OneWire.h>
#include <SD.h>
#include <MS5611.h>
#include <AccelerometerV2.h>
#include <Wire.h> b   
using namespace IntroSatLib;

float temp ;

MS5611 ms5611;

OneWire oneWire(PA11);    
DallasTemperature sensors(&oneWire);

const int PIN_CHIP_SELECT = PA4; 
File dataFile_1;
File dataFile_2;

AccelerometerV2 accel(Wire, 0x6B);


void setup() {
  Serial.begin(115200);
    
  Wire.begin();
  accel.Init();
  delay(200);

  
  Serial.print("Initializing SD card...");
  pinMode(PA4, OUTPUT); 
  if (!SD.begin(PIN_CHIP_SELECT)) {
   Serial.println("Card failed, or not present");
  } else {
    Serial.println("card initialized.");
  }
  dataFile_2 = SD.open("all.txt", FILE_WRITE);
  if (!ms5611.begin(MS5611_ULTRA_HIGH_RES)) {
   Serial.println("MS5611 failed, or not present");
   dataFile_2.println("MS5611 failed, or not present");
  } else {
    Serial.println("MS5611 initialized.");
    dataFile_2.println("MS5611 initialized.");
  }
  pinMode(PB12, OUTPUT);
  sensors.begin();
  dataFile_2.close();
}

void loop() {
  dataFile_1 = SD.open("log.txt", FILE_WRITE);
  dataFile_2 = SD.open("all.txt", FILE_WRITE);
  
  
  sensors.requestTemperatures(); 
  temp = (sensors.getTempCByIndex(0)); 
  unsigned long currentTime = millis();
  double realTemperature = ms5611.readTemperature();
  long realPressure = ms5611.readPressure();
  delay(100);
  float acc_x = accel.X();
  delay(100);
  float acc_y = accel.Y();;        
  delay(100);
  float acc_z = accel.Z();
  delay(100);

  
  Serial.print("0");  Serial.print(";");
  Serial.print(currentTime);  Serial.print(";");
  Serial.print("1000");  Serial.print(";");
  Serial.print("6000");  Serial.print(";");
  Serial.print("55.9297334");  Serial.print(";");
  Serial.print("37.6173");  Serial.print(";");
  Serial.print(realPressure);dataFile_1.print(realPressure);Serial.print(";");dataFile_1.print(";");
  Serial.print(realTemperature);dataFile_1.print(realTemperature);Serial.print(";");dataFile_1.print(";");
  Serial.print(acc_z);dataFile_1.print(acc_z);Serial.print(";");dataFile_1.print(";");
  Serial.print("1000");dataFile_1.print("1000");Serial.print(";");dataFile_1.print(";");
  Serial.print(temp);dataFile_1.print(temp);Serial.print(";");dataFile_1.print(";");
  Serial.print("1000");dataFile_1.print("1");Serial.print(";");dataFile_1.print(";");
  Serial.print("1000");dataFile_1.print("0");Serial.print(";");dataFile_1.print(";");
  Serial.print(acc_x);dataFile_1.print(acc_x);Serial.print(";");dataFile_1.print(";");
  Serial.print(acc_y);dataFile_1.print(acc_y);Serial.print(";");dataFile_1.print(";");
  Serial.print("1");dataFile_1.print("1");Serial.print(";");dataFile_1.print(";");
  Serial.print("0");dataFile_1.print("0");Serial.print(";");dataFile_1.print(";");
  
  if (temp >= 10.0){
  digitalWrite(PB12,LOW);
  Serial.print("0");            
  dataFile_1.print("0");
  }
  if (temp <= 15.0){
  digitalWrite(PB12, HIGH);
  Serial.print("1");
  dataFile_1.print("1");  
  }
  



  delay(1000); 
  dataFile_1.close();
  dataFile_2.close();
}
