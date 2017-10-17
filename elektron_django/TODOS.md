# TODOS Django Elektron:

## Recent:
	- Probar todo con dispositivos reales

## Escritura:
	- Escribir sobre el servidor y las tareas automatizadas

## Nodemcus:
	### Sensado:
		- Calibrar sensado bien por software o por hardware
	### Envio y recepción de datos:
		- Posibilidad de elegir que sea cada 1, 5, 30 o 60 segundos el envío
		- Recepción de datos para apagado prendido y configuración de tiempos
	### Configuración de conectividad:
		- Auto estado de AP si no authentica con el SSID de la EPROM
		- Paso a estado de conección
		- Posibilidad de reconfiguración de SSID, PASS e IP del server
		- Web del server AP con css bien hecha
	### Infraestructura:
		- Hacer un diseño para imprimir 3D o algo así para el circuito

## MQTT:
	- Probar todo con dispositivos reales
	- Ver seguridad MD5 salt en nodemcu y en el server.

## Controlador (views):
	- Ver que devolver en cada caso  (error con http response 505 o en la alta)
	- Chequeo de no recibir cosas en blanco ni caracteres extraños en todos los views

## Websocket:
	- Lo mismo pero con muchos devices.
	- Ver seguridad.
	- Ver si se reemplaza con mqtt

## Seguridad:
	### Server:
		- Tener cuidado con CORS
		- Tener cuidado con mqtt (SSL)
		- Tener cuidado con websocket
		- Tener cuidado con encriptacion desde nodemcu
		- Chequeo de no recibir cosas en blanco ni caracteres extraños en todos los views

## Tasks:
	- Ver si las tareas son con repetición por día o mes, tipo calendar
	- Que onda el owner??

## Costos $$ y co2:
	- Crear un modelo con vistas ABM para configurar los costos y CO2 por consumo

## Detalles:
	- Logo Elektron e íconos

## Integración:
	- Integrar Server con Ionic
	- Integrar Server con Web AngularJS
	- Integrar Server con nodemcus
