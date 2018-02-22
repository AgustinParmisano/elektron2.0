//code write by Moz for YouTube changel logMaker360, 24-11-2016
//code belongs to this video: https://youtu.be/nAUUdbUkJEI

#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ESP8266WebServer.h>

// Connect to the WiFi
const char* ssid = "depto14";                           //!!!!!!!!!!!!!!!!!!!!!
const char* password = "qawsed021188!";                //!!!!!!!!!!!!!!!!!!!!!
const char* mqtt_server = "192.168.0.21";                 //!!!!!!!!!!!!!!!!!!!!!

ESP8266WebServer server(80);
WiFiClient espClient;
PubSubClient client(espClient);

String localip = "elektronip";
String elektronname = "Elektron";
String currtime = "elektrontime";
String data = "elektrondata";

//Current Sensor ACS712 Variable Set
#define C_SENSOR1 A0
#define relay 2

//For analog read
int r1 = LOW;
int r1_received = LOW;
int incomingByte = 0;   // for incoming serial data
int c_min = 0;
int c_max = 30;


const byte ledPin = D4; // digital pin 4 on a weMos D1 mini is next to ground so easy to stick a LED in.

//OTRO ESQUEMA
//Setup variables
int numberOfSamples = 3000;

//Set Voltage and current input pins
int inPinV = 2;
int inPinI = A0;

//Calibration coeficients
//These need to be set in order to obtain accurate results
double VCAL = 1.0;
double ICAL = 1.0;
double PHASECAL = 2.3;

//Sample variables
int lastSampleV,lastSampleI,sampleV,sampleI;

//Filter variables
double lastFilteredV, lastFilteredI, filteredV, filteredI;
double filterTemp;

//Stores the phase calibrated instantaneous voltage.
double calibratedV;

//Power calculation variables
double sqI,sqV,instP,sumI,sumV,sumP;

//Useful value variables
double realPower,
       apparentPower,
       powerFactor,
       Vrms,
Irms;

void callback(char* topic, byte* payload, unsigned int length) {
 Serial.print("Message arrived [");
 Serial.print(topic);
 Serial.print("] ");
 for (int i=0;i<length;i++) {
  char receivedChar = (char)payload[i];
  Serial.print(receivedChar);
  if (receivedChar == '1')
  digitalWrite(ledPin, HIGH);
  if (receivedChar == '0')
   digitalWrite(ledPin, LOW);
  if (receivedChar == '2')
   Serial.println("Retrieve Data Forced");
  func_read_current_sensor();

  char data[80];

  String payload = "{\"ip\":\"" + localip + "\",\"time\":\"" + currtime + "\",\"name\":\"" + elektronname + "\",\"data\":\"" + apparentPower + "\"}";
  payload.toCharArray(data, (payload.length() + 1));

  Serial.print("Data to publish to client:");
  Serial.print(data);
  client.publish("esp8266status", data);
  }
  Serial.println();
}


void reconnect() {
 // Loop until we're reconnected
 while (!client.connected()) {
 Serial.print("Attempting MQTT connection...");
 // Attempt to connect
 if (client.connect("ESP8266 Client")) {
  Serial.println("connected");
  // ... and subscribe to topic
  client.subscribe("ledStatus");
 } else {
  Serial.print("failed, rc=");
  Serial.print(client.state());
  Serial.println(" try again in 5 seconds");
  // Wait 5 seconds before retrying
  delay(5000);
  }
 }
}

void setup()
{
 Serial.begin(9600);

 client.setServer(mqtt_server, 1883);
 client.setCallback(callback);

 pinMode(ledPin, OUTPUT);
 digitalWrite(ledPin, HIGH);
 client.publish("esp8266status", "Relay OFF");
 delay(5000);
 digitalWrite(ledPin, LOW);
}

void func_read_current_sensor() {
  Serial.println("func_read_current_sensor");

 for (int n=0; n<numberOfSamples; n++)
{

   //Used for offset removal
   lastSampleV=sampleV;
   lastSampleI=sampleI;

   //Read in voltage and current samples.
   sampleV = analogRead(C_SENSOR1);
   sampleI = analogRead(inPinI);

   //Used for offset removal
   lastFilteredV = filteredV;
   lastFilteredI = filteredI;

   //Digital high pass filters to remove 2.5V DC offset.
   filteredV = 0.996*(lastFilteredV+sampleV-lastSampleV);
   filteredI = 0.996*(lastFilteredI+sampleI-lastSampleI);

   //Phase calibration goes here.
   calibratedV = lastFilteredV + PHASECAL * (filteredV - lastFilteredV);

   //Root-mean-square method voltage
   //1) square voltage values
   sqV= calibratedV * calibratedV;
   //2) sum
   sumV += sqV;

   //Root-mean-square method current
   //1) square current values
   sqI = filteredI * filteredI;
   //2) sum
   sumI += sqI;

   //Instantaneous Power
   instP = calibratedV * filteredI;
   //Sum
   sumP +=instP;
}

//Calculation of the root of the mean of the voltage and current squared (rms)
//Calibration coeficients applied.
Vrms = VCAL*sqrt(sumV / numberOfSamples);
Irms = ICAL*sqrt(sumI / numberOfSamples);

//Calculation power values
realPower = VCAL*ICAL*sumP / numberOfSamples;
apparentPower = Vrms * Irms;
powerFactor = realPower / apparentPower;

//Output to serial
Serial.print(realPower);
Serial.print(' ');
Serial.print(apparentPower);
Serial.print(' ');
Serial.print(powerFactor);
Serial.print(' ');
Serial.print(Vrms);
Serial.print(' ');
Serial.println(Irms);

//Reset accumulators
sumV = 0;
sumI = 0;
sumP = 0;

}

void loop(){

  if (!client.connected()) {
  reconnect();
  }

  IPAddress ip = WiFi.localIP();
  localip = String(ip[0]) + '.' + String(ip[1]) + '.' + String(ip[2]) + '.' + String(ip[3]);
  client.loop();
  func_read_current_sensor();

  char data[80];

  String payload = "{\"ip\":\"" + localip + "\",\"time\":\"" + currtime + "\",\"name\":\"" + elektronname + "\",\"data\":\"" + apparentPower + "\"}";
  payload.toCharArray(data, (payload.length() + 1));

  Serial.print("Data to publish to client:");
  Serial.print(data);
  client.publish("esp8266status", data);
  delay(1000);
}
