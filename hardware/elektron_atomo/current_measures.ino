double medicionSensorMapeado, sensor_read;
double sensi = 0.66 // sensibilidad del sensor de +-30A = 0.66 
double VDoffset = 0.13; // ruido obtenido de mediciones con 0A
double SetV = 217.0; // voltaje fijo a falta de voltímetro, alrededor de 220 y 210 para Argentina, valor configurable a futuro.
double Imains, Irms;
double apparentPower;
float intensidadMinima=0;
float intensidadMaxima=0;

float func_read_current_sensor() {
  long tiempo=millis();
  
  while(millis()-tiempo<500) { //realizamos mediciones durante 0.5 segundos lo que serían 30 ciclos de corriente
    sensor_read = analogRead(C_SENSOR1) * (5.0 / 1023.0); //lee el valor del sensor crudo y lo mapea con los valores de voltaje entregados a la plaqueta

    //divide el valor obtenido por la sensibilidad del sensor 0.66 para +-30A
    sensor_read = sensor_read / sensi;
    
    //Obtiene los picos de la curva senoidal
    if (sensor_read>intensidadMaxima) intensidadMaxima=sensor_read;
    if (sensor_read<intensidadMinima) intensidadMinima=sensor_read;
    
    //Remueve el offset del voltaje (para elminiar ruidos del ADC, varía por plaqueta y por fabricación del sensor)
    Imains = ((intensidadMaxima - intensidadMinima) / 2) - VDoffset;
    return Imains;

  }
}

void loop(){
  float Ip = func_read_current_sensor(); 
  float Irms = Ip*0.707 // multiplicamos la corriente obtenida por 0.707 que es el RMS o valor cuadratico medio

  //Calculo de la Irms por el voltaje fijo en 217
  apparentPower = Irms * SetV;
  Serial.print(" Watios: ");
  Serial.print(apparentPower);
  Serial.print(" Voltaje: ");
  Serial.print(SetV);
  Serial.print(" Amperios: ");
  Serial.print(Irms, 4 );
  Serial.println();
}
