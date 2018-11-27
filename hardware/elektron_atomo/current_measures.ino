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
  Metro sensor_metro = Metro(0.02); //timer de 2 microsegundos.

  for  (int i = 0; i < 50; ++i) { //se toman 50 ondas.
    
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
