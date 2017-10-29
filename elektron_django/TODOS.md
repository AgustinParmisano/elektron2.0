# TODOS Django Elektron:

## Recent:
	- Armar por lo menos 3 dispositivos con sensores reales:
		- El código nuevo de los nodemcu casi andando está en éste mismo repo en la carpeta hardware: https://github.com/AgustinParmisano/elektron2.0/tree/master/hardware
		- Falta probar que sense y envíe bien (Conectar Sensor y probar MQTT)
		- Obtener mac del nodemcu y ponerlo en su subscribe y en su publish
		- Falta probar con el servidor MQTT (demonio) real, cambiar los topics del código de los nodemcus (según su mac)
	- Probar todo con varios dispositivos reales
	- Probar que funcione con ips locales
	- Probar que funcione con la ip remota

## Escritura:
	- Ver las anotaciones de Luis y Tom
	- Escribir sobre los nodemcus:
		- Como se configuran por primera vez (ssid, pass e ip)
		- Como envian los mensajes y los reciben
		- Local y Remoto
		- Tiempos de respuesta
		- Multiples dispositivos

## Nodemcus:
	- Armar 3 nuevos lo mas chicos posibles con el código viejo a ver si andan
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
	- Armar por lo menos 3 dispositivos con sensores reales:
		- El código nuevo de los nodemcu casi andando está en éste mismo repo en la carpeta hardware: https://github.com/AgustinParmisano/elektron2.0/tree/master/hardware
			- Falta probar que sense y envíe bien (Conectar Sensor y probar MQTT)
			- Falta probar que prenda y apague bien (Conectar Relé y probar MQTT)
			- Falta probar con el servidor MQTT (demonio) real, cambiar los topics del códig de los nodemcus (según su mac)
			- Ver que envíe los datos que el servidor pide (ip, mac, label, etc).
	- Probar todo con varios dispositivos reales
	- Probar que funcione con ips locales
	- Probar que funcione con la ip remota
	- Ver seguridad MD5 salt en nodemcu y en el server.
	- Se podría sacar websocket y dejar solo mqtt
	- Se puede poner ssl con mqtt
	- Se puede poner que mqtt tengo varios niveles de broker (local y remoto)
	- Se puede equality of service en los topocs (QoS) (lib) (video) http://sonoff.itead.cc/en/products/sonoff/sonoff-pow


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
