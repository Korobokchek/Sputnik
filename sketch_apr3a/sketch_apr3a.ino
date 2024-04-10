#include <DallasTemperature.h>.
#include <OneWire.h>
#include <SD.h>
#include <MS5611.h>
#include <AccelerometerV2.h>
#include <Wire.h> 
using namespace IntroSatLib;

float temp ;

String battery ;

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
   delay(100);
  } else {
    Serial.println("card initialized.");
    delay(100);
  }
  Serial.println("debug_1");
  if (!ms5611.begin(MS5611_ULTRA_HIGH_RES)) {
   Serial.println("MS5611 failed, or not present");
  } else {
    Serial.println("MS5611 initialized.");
  }
  Serial.println("debug_2");
  pinMode(PB12, OUTPUT);
  sensors.begin();
}

void loop() {
  dataFile_1 = SD.open("log.txt", FILE_WRITE);
  dataFile_2 = SD.open("all.txt", FILE_WRITE);
  
  
  sensors.requestTemperatures(); 
  temp = (sensors.getTempCByIndex(0)); 
  unsigned long currentTime = millis();
  double realTemperature = ms5611.readTemperature();
  long realPressure = ms5611.readPressure();
  double realAltitude = ms5611.getAltitude(realPressure);
  delay(100);
  float acc_x = accel.X();
  delay(100);
  float acc_y = accel.Y();;        
  delay(100);
  float acc_z = accel.Z();
  delay(100);



  if (temp >= 10.0){
  digitalWrite(PB12,LOW);
  battery = ("0");
  }
  if (temp <= 15.0){
  digitalWrite(PB12, HIGH);
  battery = ("1");
  }

  
Serial.println(String("0")+";"+
                String(currentTime)+";"+
                String("1000")+";"+
                String("6000")+";"+
                String("55.9297334")+";"+
                String("37.6173")+";"+
                String(realPressure)+";"+
                String(realTemperature)+";"+
                String(acc_z)+";"+
                String("1000")+";"+ 
                String(temp)+";"+
                String("1000")+";"+
                String("1000")+";"+
                String(acc_x)+";"+
                String(acc_y)+";"+
                String("1")+";"+
               String("0")+";"+String(battery)+";"+
               String(realAltitude));
dataFile_1.println(String("0")+";"+
               String(currentTime)+";"+
               String("1000")+";"+
               String("6000")+";"+
               String("55.9297334")+";"+
               String("37.6173")+";"+
               String(realPressure)+";"+
               String(realTemperature)+";"+
               String(acc_z)+";"+
               String("1000")+";"+
               String(temp)+";"+
               String("1000")+";"+
               String("1000")+";"+
               String(acc_x)+";"+
               String(acc_y)+";"+
               String("1")+";"+
               String("0")+";"+String(battery)+";"+
               String(realAltitude));


  delay(1000); 
  dataFile_1.close();
  dataFile_2.close();
}
