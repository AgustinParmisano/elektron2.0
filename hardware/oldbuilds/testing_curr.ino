//Definimos VARIABLES
float sensibilidad = 0.66; //5A = 180; 20A = 100; 30A = 66;
float ruido = 0.000; // filtro para eliminar ruido.
const int sensorIntensidad = A0; // Pin GPIO donde conectamos sensor.
const byte rele = D4; // Pin GPIO 4 para el relé
float valorReposo = 2.50;
float intensidadPico = 0;
float tensionDeRed = 220.0;


void setup(){
  Serial.begin(9600);
  pinMode(rele, OUTPUT);
  digitalWrite(rele, LOW);
}

void loop(){
  intensidadPico = leerCorriente();
  mostrarValores();
}

float leerCorriente()
{
  float valorVoltajeSensor;
  float corriente=0;
  long tiempo=millis();
  float intensidadMaxima=0;
  float intensidadMinima=0;
  while (millis()-tiempo<1000)//realizamos mediciones durante 0.5 segundos
  {
    valorVoltajeSensor = analogRead(sensorIntensidad) * (5.0 / 1023.0); //lectura del sensor en voltios
    corriente = corriente+((valorVoltajeSensor-valorReposo)/sensibilidad); //Ecuación para obtenr la corriente
    if (corriente>intensidadMaxima)intensidadMaxima=corriente;
    if (corriente<intensidadMinima)intensidadMinima=corriente;
    corriente = (intensidadMaxima - intensidadMinima) / 2;
  }
  return(corriente - ruido) / 10;
}

void mostrarValores()
{
    float Irms=intensidadPico*0.707;
    Serial.print("Intesidad Pico: ");
    Serial.print(intensidadPico,3);
    Serial.println("A.");
    Serial.print("Irms: ");
    Serial.print(Irms,3);
    Serial.print("A.");
    delay(100);
}
