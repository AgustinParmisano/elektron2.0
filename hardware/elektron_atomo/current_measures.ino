float func_read_current_sensor() {
  const int sensorIn = A0;
  int mVperAmp = 66; //66 para el sensor de 30A
  
  double voltage = 0;
  double VRMS = 0;
  double AmpsRMS = 0;
  float inputV = 220.0; // es la tensión que entrega la empresa distribuidora y se puede medir con otro medidor y configurarlo como parametro en el sistema por hora o por día
  unsigned int pF = 100; //como se obtiene? es el cosphi y tiene que ser por parámetro porque no podemos sacarlo para cada aparat
  float WH = 0;

  voltage = getVPP();
  VRMS = voltage  * 0.707;
  AmpsRMS = (VRMS * 1000) / mVperAmp; //pasamos los milivolts a votls multiplicando por 1000 y divimos el resultado por la sensibilidad propia del sensor según tabla del fabricante 30A = 0.66
  

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



  int maximos[50];
  int minimos[50];
  float resultMax = 0;
  float resultMin = 0;
  
  int maxValue = 0;     //pico positivo
  int minValue = 1024;     //pico negativo  
  for  (int i = 0; i < 50; ++i) {

    uint32_t start_time = millis();

    while((millis()-start_time) < 20) //muestra de 0.02 segundos que es 1 ciclo de 50Hz (ciclo de onda sinusoidal)
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
    
    maximos[i] = maxValue; //guardo los maximos de cada ciclo
    minimos[i] = minValue; //guardo los minimos de cada ciclo
    
  }

   int promMax = 0;
   int promMin = 0;
   for (int i = 0; i < 50; ++i) {
       promMax = promMax + maximos[i];
       promMin = promMin + minimos[i];
   }
   Serial.println("-----");
   Serial.println("PromMax");
   Serial.println(promMax);
   Serial.println("-----");
   Serial.println("PromMin");
   Serial.println(promMin);
   resultMax = promMax / 50; 
   resultMin = promMin / 50;
   Serial.println("-----");
   Serial.println("resultMax");
   Serial.println(resultMax);
   Serial.println("-----");
   Serial.println("resultMin");
   Serial.println(resultMin);
   Serial.println("-----");
   Serial.println("******");
  
   // Obtengo el valor medio de los picos y los mapeo a los valores del ADC del Nodemcu (que entrega y recibe 3.3v) a valores 1024 digitales.
   result = (((resultMax - resultMin) * 3.3)/1024.0) / 2.0);
   
   Serial.println();

   return result;
}
