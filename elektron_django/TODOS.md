# TODOS Django Elektron:


## Recent:
	- Cuando se edita una task pierde la cantidad de repeticiones realizadas
	- Editar DateTimeTask No funciona (cambiando device por lo menos, parece que el frontend manda otro device q el seleccionado)
	- Las tareas por valor no andan
	- Las tareas por datetime guardan mal la hora al crearlas
	- Login: investigar bien cómo es con REST y AngularJS (tal vez es mandar un token o cookie)
	- Ver lo de Seguridad en los Nodemcus: Cifrado con AES256
	- Hay un error en obtener los datos del día: si estamos a menos de 1 hora del siguiente día no obtiene bien los datos del día.
	- La IP del dispositivo puede cambiar y no se refleja en la interfaz / servidor.
	- Crear un modelo nuevo que guarde como LOGS las tareas ejecutados y su información.
	- Hacer un configurador automático de las redes para mejor testeo

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
