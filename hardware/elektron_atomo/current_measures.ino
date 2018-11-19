float func_read_current_sensor() {
  const int sensorIn = A0;
  int mVperAmp = 66; //66 para el sensor de 30A
  int samplenumber = 4000;
  double voltage = 0;
  double VRMS = 0;
  double AmpsRMS = 0;
  float inputV = 220.0; // es la tensión que entrega la empresa distribuidora y se puede medir con otro medidor y configurarlo como parametro en el sistema por hora o por día
  unsigned int pF = 99; //como se obtiene? es el cosphi y tiene que ser por parámetro porque no podemos sacarlo para cada aparato
  float WH = 0;

  voltage = getVPP();
  VRMS = (voltage / 2.0) * 0.707;
  AmpsRMS = (VRMS * 1000) / mVperAmp;
  
  if((AmpsRMS > -0.015) && (AmpsRMS < 0.008)){  // remove low end chatter
    AmpsRMS = 0.0;
  }

  WH = (inputV * AmpsRMS) * (pF / 100.0); 
  
  Serial.print(String(WH, 3)); 
  Serial.print(" WH "); 
  Serial.print(AmpsRMS);
  Serial.print(" Amps RMS");
  
  return (WH);
}


float getVPP()
{
    float result;

    int readValue;     //valor obtenido del sensor
    int maxValue = 0;     //pico positivo
    int minValue = 1024;     //pico negativo

    uint32_t start_time = millis();

    //while((millis()-start_time) < 1000) //muestra de 1 segundo
    for (int x = 0; x < samplenumber + 1; x++)
    {
       readValue = analogRead(C_SENSOR1);
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

   // Obtengo el valor medio de los picos y los mapeo a los valores del ADC del Nodemcu (que entrega y recibe 3.3v) a valores 1024 digitales.
   result = ((maxValue - minValue) * 3.3)/1024.0;
   Serial.println();

   return result;
}
