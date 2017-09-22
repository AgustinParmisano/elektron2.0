## Modelo:
  ### Datos:
  - Por ahora saltear la auth y ver como crear devices con usuario device o root y despues crear data
  - Para hacer que mqtt pueda tirar un post a rest para crear un device nuevo o para crear un dato o editar algo, hay que ver lo de la auth
  - Ver lo de permisos para mqtt (solo post desde python, alguna clave o algo que tengan los devices al enviar sus datos desde nodemcu )
  - Ver como crear datos con permisos con un POST a una URL de djangorest o con la COREAPI
  - Hacer que cuando llega un dato de un device por mqtt consulte si existe, si no existe, lo crea con un flag en False (dado de alto por user)
  - Hacer que los devices que tienen el flag dado de alto por user en True pueden enviar datos a webscoket y al mimso tiempo se almacenen en django
  - Hacer que Mqtt cree Data por POST (según Device anteriormente consultado por GET)
  - Hacer que cuando se crea un dato se consulta por la IP o ID del Device que le pertenece para
    vincularlo en la bd (es lo anterior, supuestamente)
  - Obtener datos a partir de datetime inicio y un datetime fin (recibidos por POST, mezclar con Tom).
  - Ver que funcionen todas las urls.
  - Poner permisos de owner o admin a TaskState, DeviceState y TaskFunctions (detalle)
  - Ver que en la TaskState no muestra los detalles del task bien porque no está jerarquizado bien el TaskState
    Por ejemplo: TaskState de DataTask, el detalle del Task no muestra el data_value (Preguntar a Adán)

 
  ### Estadísticas:
  - Ver cómo hacer las estadísticas, si otra app o consultar directamente a la BD.
  - Vincularla con los datos.
  - Ver cómo cruzar todo para tener estadísticas por Device, consumo y Datetime.

## BD:
 - Hacer un script para entrar a phppgmyadmin de una
 - Hacer un script para buscar devices y data en postgre 
 - Ver si hacer sqlite, sql, postgre o mongodb.
 

## MQTT:
  - Hacer que sea ordenado el envío y recepción de los datos por POST O POR RABBITMQ.

## WEBSOCKET:
  - Tener solucionadas las urls (permisos) de respuesta para websocket desde angular.

## LOGIN y AUTENTICACIÓN:
  - Una autenticación por ruta en Ionic
  - Un token de sesión validado desde el server
  - Qué onda desde websocket o ajax con angular, el token va a ser validado siempre que se haga algo (url POST/GET)
  - Encriptación?
  - Cookies? En principio no se puede
  - Cómo crear cosas pero que pida permisos?


## INTERFAZ:
  - Sección de Estadísticas
  - Sección de Programación (Tareas / Tasks)
  - Login / Autenticación - Ver como resolver lo del Token
