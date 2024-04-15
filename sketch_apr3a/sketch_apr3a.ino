#include <DallasTemperature.h>.
#include <OneWire.h>
#include <SD.h>
#include <MS5611.h>
#include <AccelerometerV2.h>
#include <Wire.h> 
#include <TinyGPSPlus.h>  
#include <SoftwareSerial.h>

using namespace IntroSatLib;

static const int RXPin = PA0, TXPin = PA1;
static const uint32_t GPSBaud = 9600;
TinyGPSPlus gps;
SoftwareSerial ss(RXPin, TXPin);

File dataFile_1;
File dataFile_2;
String valve;


HardwareSerial Serial2(PA3, PA2);

float latitude = 0;
float longitude = 0;

String battery ;

MS5611 ms5611;

OneWire oneWire(PA11);
DallasTemperature sensors(&oneWire);

const int PIN_CHIP_SELECT = PA4; 

AccelerometerV2 accel(Wire, 0x6B);

void log_data(String data, int mode) {
  if (mode == 0) {
    File debugf = SD.open("debug.txt", FILE_WRITE);
    debugf.println(data);
  } else if (mode == 1) {
    File telemetry = SD.open("telemetry.txt", FILE_WRITE);
    telemetry.println(data);
  }
  Serial.println("0;"+data);
  delay(500);
  Serial2.println("1;"+data);
  delay(500);
}

long start_pressure;

void setup() {
  digitalWrite(PB4, LOW);
  Serial.begin(115200);
  Serial2.begin(115200);
  ss.begin(GPSBaud);

  analogReadResolution(12);

  pinMode(PA0, INPUT_PULLUP);
  pinMode(PB12, OUTPUT);
    
  Wire.begin();
  accel.Init();
  delay(200);

  log_data("Initializing SD card...", 0);
  pinMode(PA4, OUTPUT); 
  if (!SD.begin(PIN_CHIP_SELECT))
    { log_data("Card failed, or not present.", 0);} 
  else 
    { log_data("card initialized.", 0); }

  delay(100);

  if (!ms5611.begin(MS5611_ULTRA_HIGH_RES))
    { log_data("MS5611 failed, or not present", 0); } 
  else 
    { log_data("MS5611 initialized.", 0); }

  sensors.begin();

  start_pressure = ms5611.readPressure();
}

float k = 0.1;  // коэффициент фильтрации, 0.0-1.0
float expRunningAverage(float newVal) {
  static float filVal = 0;
  filVal += (newVal - filVal) * k;
  return filVal;
}

double calc_amperage(int raw_input) {
  double voltage_input = raw_input*3.3/4096;
  double voltage_on_resistor = voltage_input/10;
  double amperage = voltage_on_resistor/0.05;

  return amperage;
}

double calc_voltage(int raw_input) {
  return raw_input*3.3/4096;
}

void loop() {
  double voltage = calc_voltage(analogRead(PA1));
  double amperage = calc_amperage(expRunningAverage(analogRead(PA0)));

  
  sensors.requestTemperatures(); 
  float bat_temp = sensors.getTempCByIndex(0); 
  unsigned long currentTime = millis();
  double atm_temperature = ms5611.readTemperature();
  long atm_pressure = ms5611.readPressure();
  double atm_altitude = ms5611.getAltitude(atm_pressure);
  delay(100);
  float acc_x = accel.X();
  delay(100);
  float acc_y = accel.Y();        
  delay(100);
  float acc_z = accel.Z();
  delay(100);


  if (bat_temp <= 15.0){
    digitalWrite(PB12, HIGH);
    battery = "1";
  } else {
    digitalWrite(PB12, LOW);
    battery = "0";
  }

  while (ss.available() > 0) {
      if (gps.encode(ss.read())) {
          if (gps.location.isValid()) {
              latitude = gps.location.lat();
              longitude = gps.location.lng();
          } else {
              log_data("Данные GPS недоступны", 0);
          }
      }
  }

  
  
  String data = String(currentTime) + ";" +
                String(atm_altitude) +";"+ String(atm_pressure) + ";" + String(atm_temperature) + ";" +
                String(acc_z) + ";" + String(acc_x) + ";" + String(acc_y) + ";" +
                String(bat_temp) + ";"+String(voltage)+ ";" + String(amperage) + ";" +
                valve + ";" + String(battery) +";"+ String(latitude)+";" + String(longitude) + ";";
  log_data(data, 1);
  delay(500); 
}
