const int sensorIn = A0;
int mVperAmp = 66; //66 para el sensor de 30A

double Voltage = 0;
double VRMS = 0;
double AmpsRMS = 0;
void setup(){
    Serial.begin(9600);
}

void setup(){
    Voltage = getVPP();
    VRMS = (Voltage / 2.0) * 0.707;
    AmpsRMS = (VRMS * 1000) / mVperAmp;
    Serial.print(AmpsRMS);
    Serial.print(“ Amps RMS”);
}

float getVPP()
{
    float result;

    int readValue;     //valor obtenido del sensor
    int maxValue = 0;     //pico positivo
    int minValue = 1024;     //pico negativo

    uint32_t start_time = millis();

    while((millis()-start_time) < 1000) //muestra de 1 segundo
    {
       readValue = analogRead(sensorIn);
       // se actualizan los valores pico con cada muestra
       if (readValue > maxValue) 
       {
           /*guardo el máximo valor*/
           maxValue = readValue;
       }
       if (readValue < minValue) 
       {
           /*guardo el mínimo valor*/
           minValue = readValue;
       }

    }

   // Obtengo el valor medio de los picos y los mapeo a los valores del ADC que son 1024
   result = ((maxValue - minValue) * 5.0)/1024.0;
      
   return result;
}

