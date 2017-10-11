# TODOS Django Elektron:

## Recent:
	- Crear la url y la vista de borrado de tasks (para cada una)

## Escritura:
	- Escribir sobre el servidor y las tareas automatizadas

## Tasks:
	- Ver si las tareas son con repetición por día o mes, tipo calendar
	- Que onda el owner??
	- Bash Script cada 1 segundo

## Controlador (views):
	- Crear las views (Alta, Baja, Modificación y Listar) y las urls de cada modelo.
		- Baja para cada modelo sobre todo TASKS!!! (poner la URL en el archivo de URLS.md).
	- Hacer que todas las búsquedas de datos por fecha sean por post.
	- Ver que devolver en cada caso  (error con http response 505 o en la alta)
	- Alta, Baja y Modificación con authenticación.

## Login:
	- Hacer el login y authenticación.

## MQTT:
	- Falta la vuelta desde el server a mqtt (que mqtt consulte os dispositivos apagados o prendidos)
	- Ver seguridad MD5 salt en nodemcu y en el server.

## Websocket:
	- Lo mismo pero con muchos devices.
	- Ver seguridad.

## Integración:
	- Integrar Server con Ionic
	- Integrar Server con Web AngularJS
	- Integrar Server con nodemcus

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

## Seguridad:
	### Server:
		- Tener cuidado con CORS
		- Tener cuidado con mqtt
		- Tener cuidado con websocket
		- Tener cuidado con encriptacion desde nodemcu

## Server:
	- Ver si sirve ponerle algo mejor que un simple bash

## Costos:
	- Crear un modelo con vistas ABM para configurar los costos y CO2 por consumo
