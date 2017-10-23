# TODOS Django Elektron:

## Recent:
	- Armar por lo menos 3 dispositivos con sensores reales:
		- El código nuevo de los nodemcu casi andando está en éste mismo repo en la carpeta hardware: https://github.com/AgustinParmisano/elektron2.0/tree/master/hardware
		- Los nodemcu se conectan a la red y al servidor, envían mensajes desde nodemcu al broker mqtt del servidor (forzando un subscribe por post de la url en ip/ ) pero pareciera que no hacen client.loop ya que no envian los mensajes (automaticamente) ni los reciben, tal vez hay un error en client.loop en en el subscribe. 
			- Probar: Si client.loop está corriendo bien
			- Probar: Si susbcribe está bien hecho y anda bien
			- Probar: En otros dispositivos
			- Probar: Forzar la susbcripción al igual que se fuerza la publicación, con acceso a ip/
			- Probar: Otras formas de susbcribirse o hacer el loop
	- Probar todo con varios dispositivos reales
	- Probar que funcione con ips locales
	- Probar que funcione con la ip remota

## Escritura:
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
	- Probar todo con dispositivos reales
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
