double medicionSensorMapeado, sensor_read;
double ADCvoltsperdiv = 0.0048;
double VDoffset = 2.4476; //Initial value (corrected as program runs)
double factorA = 35.8; //factorA = CT reduction factor / rsens
double SetV = 220.0;
int samplenumber = 4000;
double sumI = 0.0;
double Vadc, Vsens, Isens, Imains, sqI, Irms;
double apparentPower;
float intensidadMinima=512;
float intensidadMaxima=0;

float func_read_current_sensor() {
  i = 0; //Contador de muestras
  for (int x = 0; x < samplenumber + 1; x++) {
    sensor_read = analogRead(C_SENSOR1); //lee el valor del sensor crudo
    medicionSensorMapeado = map(sensor_read, 0, 1024, 0, 512); //mapea los valores de analog to Digital Converter de Arduino (0-1024) a los valores ADC del ESP8266/Nodemcu (0-512)

    //Voltage en ADC
    Vadc = medicionSensorMapeado * ADCvoltsperdiv;

    //Remueve el offset del voltaje (para elminiar ruidos del ADC, varía por plaqueta)
    Vsens = Vadc - VDoffset;

    //Va rectificando los picos para eliminar errores de medición aleatorios
    if (Vsens>intensidadMaxima) intensidadMaxima=Vsens;
    if (Vsens<intensidadMinima) intensidadMinima=Vsens;
    Imains = (intensidadMaxima - intensidadMinima) / 2;

    //Corriente al cuadrado
    sqI = Imains * Imains;
    //Se van acumulando las muestras de los valores de corriente instantánea obtenidos
    sumI = sumI + sqI;

  }

  //Se divide la sumatoria de los valores de corriente obtenidos en todas las muestras y se divide por la cantidad de muestras, ese valor se multiplica por el factorA
  Irms = factorA * sqrt(sumI / samplenumber); // sqrt(sumI / samplenumber) = 0,707 que es el RMS o valor cuadratico medio

  //Calculo de la Irms por el voltaje
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
