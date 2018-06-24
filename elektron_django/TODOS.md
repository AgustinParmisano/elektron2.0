# TODOS Django Elektron:

## Recent:
	- Las Tasks no andan: La data task no actualiza la fecha de ejecución y ambas no ejecutan la acción
	- Ver cuanto consume bien y cuanto es de CO2 y de guita de la lampara sola: Statistics (Setotal_data_avg puede sacar el avg de tods los datos y multiplicar la tarifa y co2 por el avg)
	- Login: poner el chequeo de tokens en todas las views que se usen desde las Interfaces
	- WebSocket tiene que destrabar la queue
	- Ver lo de Seguridad en los Nodemcus: Cifrado con AES256
	- Hay un error en obtener los datos del día: si estamos a menos de 1 hora del siguiente día no obtiene bien los datos del día.
	- Crear un modelo nuevo que guarde como LOGS las tareas ejecutados y su información.
	- Hacer un configurador automático de las redes para mejor testeo

## URLS AUTH:

// URLS Que necesitan AUTH

Login:
-------------------
http://158.69.223.78:8000/elektronusers/login


Dashboard y monitor
-------------------
http://158.69.223.78:8000/devices/
http://158.69.223.78:8000/data/totalwattstaxco2
http://158.69.223.78:8000//devices/id/lastdata/10/ o /20
ws://158.69.223.78:8888/websocket


Datatask, Datetimetask y Task Ctrl:
-------------------
http://158.69.223.78:8000/tasks/datatasks/create
http://158.69.223.78:8000/tasks/datatasks/id/updated

http://158.69.223.78:8000/tasks/datetimetasks/create
http://158.69.223.78:8000/tasks/datetimetasks/id/updated

http://158.69.223.78:8000/tasks/datatasks
http://158.69.223.78:8000/tasks/datetimetasks

http://158.69.223.78:8000/tasks/type/id/remove


Components y component Ctrl:
------------------
http://158.69.223.78:8000/devices/id/

http://158.69.223.78:8000/devices/id/turnon
http://158.69.223.78:8000/devices/id/shutdown

http://158.69.223.78:8000/devices/id/enable
http://158.69.223.78:8000/devices/id/disable

http://158.69.223.78:8000/devices/id/updatelabel


StatisticsCtrl y HistoryCtrl
------------------
http://158.69.223.78:8000/devices/statistics
http://158.69.223.78:8000/devices/31/data/21/05/2018/18/22/05/2018/14/perday/1/5/1/ (por dia)
http://158.69.223.78:8000/devices/31/data/21/05/2018/18/22/05/2018/14/perhour/1/5/1/ (por hora)

## Nodemcus:
	- Armar 3 nuevos lo mas chicos posibles con el código viejo a ver si andan
	### Envio y recepción de datos:
		- Posibilidad de elegir que sea cada 1, 5, 30 o 60 segundos el envío
		- Recepción de datos para apagado prendido y configuración de tiempos
	### Configuración de conectividad:
		- Auto estado de AP si no authentica con el SSID de la EPROM
		- Paso a estado de conexión
		- Posibilidad de reconfiguración de SSID, PASS e IP del server
		- Web del server AP con css bien hecha
	### Infraestructura:
		- Hacer un diseño para imprimir 3D o algo así para el circuito

## MQTT:
	- Armar por lo menos 3 dispositivos con sensores reales:
	- Probar todo con varios dispositivos reales
	- Ver seguridad MD5 salt en nodemcu y en el server.
	- Se podría sacar websocket y dejar solo mqtt
	- Se puede poner ssl con mqtt
	- Se puede quality of service en los topocs (QoS) (lib) (video) http://sonoff.itead.cc/en/products/sonoff/sonoff-pow

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
		- Tener cuidado con mqtt (va crudo, SSL)
		- Tener cuidado con websocket
		- Tener cuidado con encriptacion desde nodemcu
		- Chequeo de no recibir cosas en blanco ni caracteres extraños en todos los views

## Tasks:
	- Que onda el owner??

## Costos $$ y co2:
	- Crear un modelo con vistas ABM para configurar los costos y CO2 por consumo

## Detalles:
	- Logo Elektron e íconos
