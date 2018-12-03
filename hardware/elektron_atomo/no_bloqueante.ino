#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <EEPROM.h>
#include <PubSubClient.h>
#include <Metro.h>

char* ssid = "test";
char* password = "12345678";
String st;
String content;
int statusCode;
int auxwebtype;

String qurl;
String qsid;

String equrl;
String esid;

String apiurl;
String mqtt_server;                 //!!!!!!!!!!!!!!!!!!!!!

ESP8266WebServer server(80);
WiFiClient espClient;
PubSubClient client(espClient);

String localip = "elektronip";
String elektronname = "Elektron";
String currtime = "elektrontime";
String mac = "elektronmac";
float data = 1;

//Current Sensor ACS712 Variable Set
#define C_SENSOR1 A0
const byte rele = D4; // digital pin 4 on a weMos D1 mini is next to ground so easy to stick a LED in.

//For analog read
int r1 = LOW;
int r1_received = LOW;
int incomingByte = 0;   // for incoming serial data
int c_min = 0;
int c_max = 30;

//For analog read
double valorVoltajeSensor, sensor_read;

float ruido;

//Constants to convert ADC divisions into mains current values.
double ADCvoltsperdiv = 0.0048;
//double ADCvoltsperdiv = 0.011;
double VDoffset = 2.4476; //Initial value (corrected as program runs)

//Equation of the line calibration values
//double factorA = 15.35; //factorA = CT reduction factor / rsens
double factorA = 35.8; //factorA = CT reduction factor / rsens
double Ioffset = 0;

//Constants set voltage waveform amplitude.
double SetV = 220.0;

//Counter
int counter = 0;

int samplenumber = 4000;
int i = 0;

//Used for calculating real, apparent power, Irms and Vrms.
double sumI = 0.0;

int sum1i = 0;
double sumVadc = 0.0;

double Vadc, Vsens, Isens, Imains, sqI, Irms;
double apparentPower;

//NODEMCU ESP8266-12 VALUES MAPPING!!!//
int val;
int device_state = 0;
int first_time = 1;
int setup_retries = 0;
float power_data = 0;
int pub_status;

boolean mqtt_state = false;
Metro mqtt_metro = Metro(10);


void callback(char* topic, byte* payload, unsigned int length) {
  char data[300];
  char topic_char[50];

  if(mqtt_metro.check()) {

    mqtt_state = !mqtt_state;

    Serial.print("Message arrived [");
    Serial.println(topic);
    Serial.print("] ");

    for (int i = 0; i < length; i++) {
      char receivedChar = (char)payload[i];
      Serial.print("MSG RECEIVED!!!!!!!!!!  ");
      Serial.println(receivedChar);

      //Shutdown device
      if (receivedChar == '1') {
        Serial.println("Shutdown Device");
        digitalWrite(rele, HIGH);
        device_state = 1;
        power_data = 0;
        String payload = "{\"ip\":\"" + localip + "\",\"mac\":\"" + mac + "\",\"label\":\"" + elektronname + "\",\"data_value\":\"" + power_data + "\",\"state\":\"" + device_state + "\"}";
        payload.toCharArray(data, (payload.length() + 1));

        pub_status = client.publish(topic_char, data);
        Serial.println("PUB STATUS");
        Serial.println(pub_status);

        while (pub_status == 0) {
          Serial.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
          Serial.println("Decive MQTT STOPPED PUBLISHING DATA!!!");
          Serial.println("RECONNECTING TO MQTT SERVER BROKER");
          Serial.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
          mqtt_start();
          pub_status = client.publish(topic_char, data);
          Serial.println("PUB STATUS");
          Serial.println(pub_status);
          delay(1000);
          reconnect();
        }

      }

      //Turn on device
      if (receivedChar == '0') {
        Serial.println("Turnon Device");
        digitalWrite(rele, LOW);
        device_state = 0;
      }

    }
    Serial.println();
    }
}


String clientId = "ESP8266Client-";
String mini_mac = mac.substring(mac.length() - 5);

int reconnection_tries = 0;
void reconnect() {
  char topic_char[50];

  // Loop until we're reconnected
  Serial.println("Checking MQTT connection...");
  Serial.println(client.connected());

  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    clientId += String(random(0xffff), HEX);

    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // ... and subscribe to topic
      //mini_mac = mac.substring(11);
      mini_mac = mac.substring(mac.length() - 5);
      String topic = "elektron/" + mini_mac + "/new_order";
      topic.toCharArray(topic_char, (topic.length() + 1));

      client.subscribe(topic_char);
      Serial.println("Subscribing to mini mac based topic: ");
      Serial.println(topic_char);

    } else {

      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
      reconnection_tries += 1;
      if (reconnection_tries > 5) {
        reconnection_tries = 0;
        Serial.println("Failed 5 times, trying connection to wifi network");
        //testWifi();
        setup();
      }
    }
  }
}

int interrupt = 0;
int wait = 5;

void setup() {
  Serial.begin(9600);

  pinMode(rele, OUTPUT);
  digitalWrite(rele, HIGH);
  delay(5000);
  //digitalWrite(rele, LOW);

  EEPROM.begin(512);
  delay(10);

  Serial.println();
  Serial.println();
  Serial.println("Startup");
  device_state = 1;
  first_time = 1;

  // read eeprom for ssid and pass
  Serial.println("Reading EEPROM ssid");
  esid = "";
  for (int i = 0; i < 32; ++i)
  {
    esid += char(EEPROM.read(i));
  }
  Serial.print("SSID: ");
  Serial.println(esid);

  Serial.println("Reading EEPROM pass");
  String epass = "";
  for (int i = 32; i < 64; ++i)
  {
    epass += char(EEPROM.read(i));
  }
  Serial.print("PASS: ");
  Serial.println(epass);

  Serial.println("Reading EEPROM Server URL");
  mqtt_server = "";
  for (int i = 64; i < 128; ++i)
  {
    //equrl += char(EEPROM.read(i));
    mqtt_server += char(EEPROM.read(i));
  }
  Serial.print("URL: ");
  Serial.println(mqtt_server);
  char mqtt_server_char[50];
  mqtt_server.toCharArray(mqtt_server_char, 50);
  Serial.print("MQTT BROKER IP (CHAR): ");
  Serial.println(mqtt_server_char);
  client.setCallback(callback);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  // If SSID is set then start web mode 0 (web server mode)
  if ( esid.length() > 1 ) {
    WiFi.begin(esid.c_str(), epass.c_str());
    if (testWifi()) {
      launchWeb(0);
      return;
    }
  }
  //If not connects to AP set up its own, start web mode 1

  if (setup_retries < 1){
    setup_retries += 1;
    Serial.println("Connect timed out, retrying setup");
    delay(1000);
    setup();
  }
  Serial.println("Connect timed out, opening AP");
  setupAP();
}

//test wifi to connect configured SSID AP
bool testWifi(void) {
  int c = 0;
  Serial.println("Waiting for Wifi to connect");
  while ( c < 45 ) {
    if (WiFi.status() == WL_CONNECTED) {
      return true;
    }
    delay(500);
    Serial.print(WiFi.status());

    c++;
  }
  Serial.println("Cannot connect to WIFI");
  return false;
}

void launchWeb(int webtype) {
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("Local IP: ");
  Serial.println(WiFi.localIP());
  Serial.print("SoftAP IP: ");
  Serial.println(WiFi.softAPIP());
  IPAddress ip = WiFi.localIP();
  localip = String(ip[0]) + '.' + String(ip[1]) + '.' + String(ip[2]) + '.' + String(ip[3]);
  mac = WiFi.macAddress();

  if (localip != "0.0.0.0") {
    Serial.println("Local IP is NOT 0.0.0.0 so show main page: web mode 0 (connecting to configured SSID AP and start web server)");
    createWebServer(0);
    mqtt_start();
  } else {
    Serial.println("Local IP is 0.0.0.0 so show SSID, PASS & URL configuration web: web mode 1");
    func_cleareeprom();
    createWebServer(1);

  }

  // Start the server
  server.begin();
  Serial.println("Server started");
}

bool ok = false; //False until mqtt server is on and connected correctly with the device
void mqtt_start() {
  char topic_char[50];
  char mqtt_server_char[50];
  String mini_mac;

  Serial.println("Starting MQTT On Device Client");

  mqtt_server.toCharArray(mqtt_server_char, 50);

  Serial.print("MQTT BROKER IP: ");
  Serial.println(mqtt_server_char);

  client.setServer(mqtt_server_char, 1883);
  client.setCallback(callback);
  mini_mac = mac.substring(mac.length() - 5);

  String topic = "elektron/" + mini_mac + "/new_order";
  topic.toCharArray(topic_char, (topic.length() + 1));
  client.subscribe(topic_char);

  Serial.println("Subscribing to mini mac based topic: ");
  Serial.println(topic_char);
  //client.publish("sensors/new_data", "Relay OFF");

  if (!client.connected()) {
    reconnect();
  }

  IPAddress ip = WiFi.localIP();
  localip = String(ip[0]) + '.' + String(ip[1]) + '.' + String(ip[2]) + '.' + String(ip[3]);
  Serial.print("Local IP: ");
  Serial.println(localip);
  client.loop();

  ok = true;
}

//function to start AP mode
void setupAP(void) {
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  int n = WiFi.scanNetworks();
  Serial.println("scan done");
  if (n == 0)
    Serial.println("no networks found");
  else
  {
    Serial.print(n);
    Serial.println(" networks found");
    for (int i = 0; i < n; ++i)
    {
      // Print SSID and RSSI for each network found
      Serial.print(i + 1);
      Serial.print(": ");
      Serial.print(WiFi.SSID(i));
      Serial.print(" (");
      Serial.print(WiFi.RSSI(i));
      Serial.print(")");
      Serial.println((WiFi.encryptionType(i) == ENC_TYPE_NONE) ? " " : "*");
      delay(10);
    }
  }
  Serial.println("");
  st = "<ol>";
  for (int i = 0; i < n; ++i)
  {
    // Print SSID and RSSI for each network found
    st += "<li>";
    st += WiFi.SSID(i);
    st += " (";
    st += WiFi.RSSI(i);
    st += ")";
    st += (WiFi.encryptionType(i) == ENC_TYPE_NONE) ? " " : "*";
    st += "</li>";
  }
  st += "</ol>";
  delay(100);
  WiFi.softAP(ssid, password, 6);
  Serial.println("softap");

  IPAddress ip = WiFi.softAPIP();
  String ipStr = String(ip[0]) + '.' + String(ip[1]) + '.' + String(ip[2]) + '.' + String(ip[3]);
  launchWeb(1);
  Serial.println("over");
}

//function to create web server
void createWebServer(int webtype)
{
  Serial.println("If Webtype is 1 Configure SSID & PASS if is 0 show local IP: Webtype is:");
  Serial.println(webtype);
  auxwebtype = webtype;
  delay(5000);
  if ( webtype == 1 ) {
    Serial.println("CONFIGURING SSID CONNECTION");
    server.on("/", []() {
      if ( auxwebtype == 1 ) {
        Serial.println("CONFIGURING SSID CONNECTION STARTING");
        IPAddress ip = WiFi.softAPIP();
        String ipStr = String(ip[0]) + '.' + String(ip[1]) + '.' + String(ip[2]) + '.' + String(ip[3]);
        content = "<!DOCTYPE HTML>\r\n<html>Hello from ESP8266 at ";
        content += ipStr;
        content += "<p>";
        content += st;
        content += "</p><form method='get' action='setting'><label>SSID: </label><input name='ssid' length=32><label>PASS: </label><input name='pass' length=64><label>SERVER URL: </label><input name='url' length=64><input type='submit'></form>";
        content += "</html>";
        Serial.println("Sending configuration data");
        server.send(200, "text/html", content);
        content = "";
      } else if ( auxwebtype == 0 ) {
        IPAddress ip = WiFi.localIP();
        String ipStr = String(ip[0]) + '.' + String(ip[1]) + '.' + String(ip[2]) + '.' + String(ip[3]);
        server.send(200, "text/html", "Second Stage {\"IP\":\"" + ipStr + "\"}");
      }
    });
    server.on("/setting", []() {
      qsid = server.arg("ssid");
      String qpass = server.arg("pass");
      qurl = server.arg("url");

      if (qsid.length() > 0 && qpass.length() > 0 && qurl.length() > 0) {
        Serial.println("clearing eeprom");
        for (int i = 0; i < 128; ++i) {
          EEPROM.write(i, 0);
        }
        Serial.println(qsid);
        Serial.println("");
        Serial.println(qpass);
        Serial.println("");
        Serial.println(qurl);
        Serial.println("");

        Serial.println("writing eeprom ssid:");
        for (int i = 0; i < qsid.length(); ++i)
        {
          EEPROM.write(i, qsid[i]);
          Serial.print("Wrote: ");
          Serial.println(qsid[i]);
        }
        Serial.println("writing eeprom pass:");
        for (int i = 0; i < qpass.length(); ++i)
        {
          EEPROM.write(32 + i, qpass[i]);
          Serial.print("Wrote: ");
          Serial.println(qpass[i]);
        }
        Serial.println("writing eeprom url:");
        for (int i = 0; i < qurl.length(); ++i)
        {
          EEPROM.write(64 + i, qurl[i]);
          Serial.print("Wrote: ");
          Serial.println(qurl[i]);
        }
        EEPROM.commit();
        content = "{\"Success\":\"saved to eeprom... reset to boot into new wifi\"}";
        statusCode = 200;
        Serial.println("stoping AP mode . . .");
        WiFi.mode(WIFI_STA);
        Serial.println("AP mode Stopped");
        setup();
      } else {
        content = "{\"Error\":\"404 not found\"}";
        statusCode = 404;
        Serial.println("Sending 404");
      }
      server.send(statusCode, "application/json", content);
    });
  } else if (webtype == 0) {

    Serial.println("stoping AP mode . . .");
    WiFi.mode(WIFI_STA);
    Serial.println("AP mode Stopped");

    char connected_ssid[80];
    esid.toCharArray(connected_ssid, 80);

    Serial.println("CONNECTED TO SSID: ");
    Serial.println(connected_ssid);


    server.on("/", []() {
      client.publish("sensors/new_data", "TESTING MQTT FROM NODEMCU");
      IPAddress ip = WiFi.localIP();
      String ipStr = String(ip[0]) + '.' + String(ip[1]) + '.' + String(ip[2]) + '.' + String(ip[3]);
      server.send(200, "text/html", "{\"IP\":\"" + ipStr + "\"}");
    });

    server.on("/cleareeprom", []() {

      func_cleareeprom();

    });
    server.on("/disconnect", []() {

      func_disconnect();

    });

  }
}

void func_disconnect() {
  //Disconnect from configured SSID AP and setup owns AP again web mode 1
  content = "<!DOCTYPE HTML>\r\n<html>";
  content += "<p>Disconecting</p></html>";
  server.send(200, "text/html", content);
  Serial.println("disconecting . . .");
  WiFi.disconnect();
  Serial.println("Disconected");
  //setup owns AP again web mode 1
  setupAP();
}

void func_cleareeprom() {
  //Clear EEPROM to restart ESP default values
  content = "<!DOCTYPE HTML>\r\n<html>";
  content += "<p>Clearing the EEPROM</p></html>";
  server.send(200, "text/html", content);
  Serial.println("clearing eeprom");
  for (int i = 0; i < 128; ++i) {
    EEPROM.write(i, 0);
  }
  EEPROM.commit();
  Serial.println("eeprom cleared...");
}

void func_configuration_mode() {
  Serial.println("CONFIGURING SSID CONNECTION");
  Serial.println("CONFIGURING SSID CONNECTION STARTING");
  IPAddress ip = WiFi.softAPIP();
  String ipStr = String(ip[0]) + '.' + String(ip[1]) + '.' + String(ip[2]) + '.' + String(ip[3]);
  content = "<!DOCTYPE HTML>\r\n<html>Hello from ESP8266 at ";
  content += ipStr;
  content += "<p>";
  content += st;
  content += "</p><form method='get' action='setting'><label>SSID: </label><input name='ssid' length=32><label>PASS: </label><input name='pass' length=64><label>SERVER URL: </label><input name='url' length=64><input type='submit'></form>";
  content += "</html>";
  Serial.println("Sending configuration data");
  server.send(200, "text/html", content);
  content = "";
  return;
}

float func_read_current_sensor() {
       const int sensorIn = A0; //pin ADC del Nodemcu.
        int mVperAmp = 66; //Sensibilidad del sensor de 30A según fabricante.
        double voltage = 0;
        double VRMS = 0;
        double AmpsRMS = 0;
        float inputV = 220.0; //tensión de la red, podría ser enviado por parámetro para achicar el error. 
        unsigned int pF = 100; //factor de potencia con coseno de Phi en 1.
        float WH = 0;
        voltage = getVPP(); //se obtiene la corriente media.
        VRMS = voltage * 0.707; //se multiplica la corriente eficaz obtenida por valor cuadrático medio.
        AmpsRMS = (VRMS * 1000) / mVperAmp; //se multiplica el voltaje RMS por mil para pasar de milivolts a volts y se divide por la sensibilidad del sensor.
       
        WH = (inputV * AmpsRMS) * (pF / 100.0); //se multiplica la corriente eficaz por la tensión y el resultado por el factor de potencia (1 en nuestro caso) para obtener la potencia aparente.
       
        return (WH); //se retorna la potencia aparente para ser enviada al sistema.
      }



float getVPP()
{
  float result;
  int readValue;     
  int maximos[50];
  int minimos[50];
  float resultMax = 0;
  float resultMin = 0;
  Metro sensor_metro = Metro(1000); //timer de 2 microsegundos.
  int i = 0;

  uint32_t start_time_sec = millis(); //milisegundos actuales.

  while((millis()-start_time_sec) < 500) { //se toman 50 ondas.
    
    int maxValue = 0;     
    int minValue = 1024;      
    uint32_t start_time = millis(); //milisegundos actuales.
    
    if(sensor_metro.check()) {
           while((millis()-start_time) < 20) //muestreo durante 0.02 segundos.
           {
         
               readValue = analogRead(C_SENSOR1); //se lee del sensor.
                if (readValue > maxValue)
               {
                        maxValue = readValue; //pico máximo de la onda actual.
                }
                if (readValue < minValue)
                    {
                        minValue = readValue; //pico mínimo (negativo) de la onda actual.
                    }
           }
           if (i < 50){
            i = i +1;
           }else{
            i = 0;
           }
    }
    maximos[i] = maxValue; //se guardan los picos en sus arreglos.
    minimos[i] = minValue;
    
  }

   //se promedia cada pico.
   int promMax = 0;
   int promMin = 0;
   for (int i = 0; i < 50; ++i) { 
       promMax = promMax + maximos[i]; 
       promMin = promMin + minimos[i];
   }
   
   resultMax = promMax / 50;
   resultMin = promMin / 50;
 
   //se restan los promedios de los picos, los convierto a valores digitales según el voltaje del Nodemcu y los divido por 2 para tener su media (los picos mínimos son negativos por lo que se suman a los positivos en la resta).
   result = ((((resultMax - resultMin) * 3.3)/1024.0) / 2.0);
   
   return result;
}

unsigned long previousMillis = 0;        // will store last time LED was updated
const long interval = 5000;           // interval at which to blink (milliseconds)

boolean sensor_state = false;
Metro sensor_metro = Metro(1000);

int divs = 1;

void loop() {

  server.handleClient();

  if (ok == true) {
    if(sensor_metro.check()) {
      client.loop();
      String topic = "sensors/new_data";
      char topic_char[50];
      char data[300];
      topic.toCharArray(topic_char, (topic.length() + 1));
      unsigned long currentMillis = millis();

      if (first_time == 1){
        power_data = 0;
        device_state = 1;
        String payload = "{\"ip\":\"" + localip + "\",\"mac\":\"" + mac + "\",\"label\":\"" + elektronname + "\",\"data_value\":\"" + power_data + "\",\"state\":\"" + device_state + "\"}";
        payload.toCharArray(data, (payload.length() + 1));

    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // ... and subscribe to topic
      //mini_mac = mac.substring(11);
      mini_mac = mac.substring(mac.length() - 5);
      String topic = "elektron/" + mini_mac + "/new_order";
      topic.toCharArray(topic_char, (topic.length() + 1));

      client.subscribe(topic_char);
      Serial.println("Subscribing to mini mac based topic: ");
      Serial.println(topic_char);

    } else {

      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
      reconnection_tries += 1;
      if (reconnection_tries > 5) {
        reconnection_tries = 0;
        Serial.println("Failed 5 times, trying connection to wifi network");
        //testWifi();
        setup();
      }
    }


        pub_status = client.publish(topic_char, data);
        Serial.println("PUB STATUS");
        Serial.println(pub_status);



        first_time = 0;
        digitalWrite(rele, HIGH);

        while (pub_status == 0) {
          Serial.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
          Serial.println("Decive MQTT STOPPED PUBLISHING DATA!!!");
          Serial.println("RECONNECTING TO MQTT SERVER BROKER");
          Serial.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
          mqtt_start();
          pub_status = client.publish(topic_char, data);
          Serial.println("PUB STATUS");
          Serial.println(pub_status);
          delay(1000);
          reconnect();
        }


      }

      if (device_state == 0) {


        if (first_time == 0) {

            power_data += func_read_current_sensor();
            divs += 1;
          //delay(1);

          if (currentMillis - previousMillis >= interval) {
            previousMillis = currentMillis;
            power_data = power_data / divs;
            if (power_data > 5000) {
              power_data = 0;
            }

            //String payload = "{\"device_ip\":\"" + localip + "\",\"device_mac\":\"" + mac + "\",\"label\":\"" + "AAAAAAAA" + "\",\"data_value\":\"" + power_data + "\"}";
            String payload = "{\"ip\":\"" + localip + "\",\"mac\":\"" + mac + "\",\"label\":\"" + elektronname + "\",\"data_value\":\"" + power_data + "\",\"state\":\"" + device_state + "\"}";
            payload.toCharArray(data, (payload.length() + 1));


            pub_status = client.publish(topic_char, data);
            Serial.println("PUB STATUS");
            Serial.println(pub_status);


            while (pub_status == 0) {
              Serial.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
              Serial.println("Decive MQTT STOPPED PUBLISHING DATA!!!");
              Serial.println("RECONNECTING TO MQTT SERVER BROKER");
              Serial.println("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!");
              mqtt_start();
              pub_status = client.publish(topic_char, data);
              Serial.println("PUB STATUS");
              Serial.println(pub_status);
              delay(1000);
              reconnect();
            }

            Serial.print("Data to publish to client by loop:");
            Serial.println(data);
            Serial.println("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-");


            divs = 1;
          }
        }else{
          power_data = 0;
          first_time = 0;
        }

      }
    }
  }
}
