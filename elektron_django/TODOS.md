# TODOS Django Elektron:

## Recent:
	- Handler de datatask: ejecutar task function y cambiar la task de estado a done

## Escritura:
	- Escribir sobre el servidor

## Tasks:
	- Cuando una tarea se ejecuta, que hacemos? se pone en terminada y listo?
	- Terminar el handler de tasks
		- data task
		- datetime task
	- Que los levante cron cada 1 minuto

## Model:
	- Crear las vistas (Alta, Baja, Modificación y Listar) y las urls de cada modelo.
		- Modificacion para devices y tasks (por ejemplo ponerle enabled/disabled a un device)
		- Baja para cada modelo (poner la URL en el archivo de URLS.md).
	- Ver como hacer las tareas automatizadas:
		- DataTasks (Celery o Cron)
		- DateTimeTasks (Celery o Cron)
	- Alta, Baja y Modificacion con authenticación.
	- Ver si las tareas son con repeticion por dia o mes, tipo calendar
	- Ver que devolver en cada caso  (error o hit)
	- Ver como enviar las date_to y la date_from de los datetimestasks

## Login:
	- Hacer el login y authenticación.

## MQTT:
	- Falta la vuelta desde el server a mqtt
	- Ver seguridad MD5 salt en nodemcu y en el server.

## Websocket:
	- Ver como integrar websocket para enviar los datos de un device en tiempo real.
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
	- Ver si sirve ponerle algo mejor que un simple ssh
