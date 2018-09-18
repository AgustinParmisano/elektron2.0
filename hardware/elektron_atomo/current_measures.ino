double medicionSensorMapeado, sensor_read;
double VDoffset = 2.4476; //Initial value (corrected as program runs)
double SetV = 217.0;
int samplenumber = 4000;
double sumI = 0.0;
double Imains, Irms;
double apparentPower;
float intensidadMinima=512;
float intensidadMaxima=0;

float func_read_current_sensor() {
  long tiempo=millis();
  
  while(millis()-tiempo<500) { //realizamos mediciones durante 0.5 segundos lo que serían 30 ciclos de corriente
    sensor_read = analogRead(C_SENSOR1) * (5.0 / 1023.0); //lee el valor del sensor crudo

    //Obtiene los picos de la curva senoidal
    if (sensor_read>intensidadMaxima) intensidadMaxima=sensor_read;
    if (sensor_read<intensidadMinima) intensidadMinima=sensor_read;
    
    //Remueve el offset del voltaje (para elminiar ruidos del ADC, varía por plaqueta)
    Imains = ((intensidadMaxima - intensidadMinima) / 2) - VDoffset;


  }
}

void loop(){
  //Se divide la sumatoria de los valores de corriente obtenidos en todas las muestras y se divide por la cantidad de muestras, ese valor se multiplica por el factorA
  float Ip = func_read_current_sensor(); 
  float Irms = Ip*0.707 // multiplicamos la corriente obtenida por 0.707 que es el RMS o valor cuadratico medio

  //Calculo de la Irms por el voltaje fio en 217
  apparentPower = Irms * SetV;
  Serial.print(" Watios: ");
  Serial.print(apparentPower);
  Serial.print(" Voltaje: ");
  Serial.print(SetV);
  Serial.print(" Amperios: ");
  Serial.print(Irms, 4 );
  Serial.println();

  //Reset values ready for next sample.
  sumI = 0.0;
  return(apparentPower);
}
