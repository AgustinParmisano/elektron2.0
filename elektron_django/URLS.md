## URLS Nuevas:
	- http://elektron20.ddns.net:8000/devices/43/data/08/02/2018/07/03/2018/1/50/1/
	- http://elektron20.ddns.net:8000/devices/43/data/08/02/2018/10/07/03/2018/20/1/10/1/
	- http://elektron20.ddns.net:8000/devices/43/data/08/02/2018/10/07/03/2018/20/perhour/1/10/1/
	- http://elektron20.ddns.net:8000/devices/43/data/08/02/2018/10/07/03/2018/20/perday/1/10/1/


## Use with python resquests:

```
import requests
```

### Authentication (se debe guardar la sesion s = requests.Session() y luego usarse la sesion logeada para guardar las credenciales ):
  ## Login (post)
  ```
  user = {'username':'root','password':'password'}
  s = requests.Session()
  s.post("http://localhost:8000/elektronusers/login", data=user)
  r.text
  r.url
  ```

  ## Logout (get)
  ```
  requests.get("http://localhost:8000/elektronusers/logout")
  r.text
  r.url
  ```

### Data from devices:

```
{"device_ip": '10.0.0.8',"device_mac": "11:11:55:55","label": "lavarropas","devicestate": 1, "data_value": 76}
```

### Devices:

  - Create Device:
    - post:
    ```
    data = {'device_ip': '110.0.0.11', 'device_mac': '12:52:12:92', 'devicestate': 1, 'label': 'dispo2'}
    r = requests.post("http://localhost:8000/devices/create", data=data)
    r.text
    r.url
    ```

  - Update Device:
  ```
  data = {'device_ip': '110.0.0.11', 'device_mac': '12:52:12:92', 'devicestate': 1, 'label': 'dispo2', 'owner': 'root'}
  r = requests.post("http://localhost:8000/devices/update", data=data)
  r.text
  r.url
  ```

  - List Devices:
  ```
  r = requests.get("http://localhost:8000/devices/")
  r.text
  r.url
  ```

  - Device Detail:
  ```
  r = requests.get("http://localhost:8000/devices/<device_id>")
  r.text
  r.url
  ```

  - Device <id> Data:
  ```
  r = requests.get("http://localhost:8000/devices/<device_id>/data")
  r.text
  r.url
  ```

  - Device <id> Data en un dia especifico (dd/mm/yyyy):
  ```
  r = requests.get("http://localhost:8000/devices/<device_id>/data/dd/mm/yyyy")
  r.text
  r.url
  ```

  - Device <id> Data en un rango de dias especificos (dd/mm/yyyy/dd/mm/yyyy):
  ```
  r = requests.get("http://localhost:8000/devices/<device_id>/data/dd1/mm1/yyyy1/dd2/mm2/yyyy2")
  r.text
  r.url
  ```

  - Device <id> Data en una hora de una fechaespecifica (dd/mm/yyyy/hh):
  ```
  r = requests.get("http://localhost:8000/devices/<device_id>/data/dd/mm/yyyy/hh")
  r.text
  r.url
  ```

  - Device <id> Data en un rango de fechas especificas (dd/mm/yyyy/hh/dd/mm/yyyy/hh):
  ```
  r = requests.get("http://localhost:8000/devices/<device_id>/data/dd1/mm1/yyyy1/hh1/dd2/mm2/yyyy2/hh2")
  r.text
  r.url
  ```

  - Device devices/<device_id>/shutdown enviar mensaje de apagado al dispositivo:
  ```
  r = requests.get("http://localhost:8000/devices/<device_id>/shutdown")
  r.text
  r.url
  ```

  - Device devices/<device_id>/turnon enviar mensaje de apagado al dispositivo:
  ```
  r = requests.get("http://localhost:8000/devices/<device_id>/turnon")
  r.text
  r.url
  ```

  - Device devices/<device_id>/updatelabel cambia el label al dispositivo:
  ```
  data = {'label': 'dispo2'}
  r = requests.post("http://localhost:8000/devices/<device_id>/updatelabel", data=data)
  r.text
  r.url
  ```

  - Device devices/<device_id>/enable cambia el estado del dispositivo:
    - POST
    ```
    data = {}
    r = requests.post("http://localhost:8000/devices/<device_id>/enable", data=data)
    r.text
    r.url
    ```

  - Device devices/<device_id>/disable cambia el estado del dispositivo:
    - POST
    ```
    data = {}
    r = requests.post("http://localhost:8000/devices/<device_id>/disable", data=data)
    r.text
    r.url
    ```

### Data:

  - Create Data:
    - post:
    ```
    data = {'data_value':'9999', 'date':'', 'device':'9', 'device_ip':'10.0.0.4', 'device_mac':'33:33:22:22', 'label':'pava electrica'}
    r = requests.post("http://localhost:8000/data/create", data=data)
    r.text
    r.url
    ```

  - Update Data:
    Data should not update.

  - List Data:
  ```
  r = requests.get("http://localhost:8000/data/")
  r.text
  r.url
  ```

  - Data Detail:
  ```
  r = requests.get("http://localhost:8000/data/<data_id>")
  r.text
  r.url
  ```

  - Data en un Dia especifico [corchetes = opcional]:
    ```
    r = requests.get("http://localhost:8000/data/dd/mm/yyyy")
    r.text
    r.url
    ```

  - Data en una Fecha y hora especificas (dd/mm/yyyy/hh):
  ```
  r = requests.get("http://localhost:8000/data/dd/mm/yyyy/hh")
  r.text
  r.url
  ```

  - Data en un Mes especifico:
  ```
  r = requests.get("http://localhost:8000/data/mm/yyyy")
  r.text
  r.url
  ```

  - Data en un rango de fechas especificas (dd1/mm1/yyyy1/ y dd2/mm2/yyyy2):
  ```
  r = requests.get("http://localhost:8000/data/dd1/mm1/yyyy1/dd2/mm2/yyyy2/")
  r.text
  r.url
  ```

  - Data en un rango de fechas especificas y horas (dd1/mm1/yyyy1/hh1 y dd2/mm2/yyyy2/hh2):
  ```
  r = requests.get("http://localhost:8000/data/dd1/mm1/yyyy1/hh1/dd2/mm2/yyyy2/hh2")
  r.text
  r.url
  ```

  - Data en una fecha y hora especifica según Device por POST en el cuerpo opcional [corchetes = opcional]
    - post:
    ```
    data = {'hour': [hour],'day': [dia], 'month': [mes], 'year': [year], 'device_id': [pk]'}
    r = requests.post("http://localhost:8000/data/date", data)
    r.text
    r.url
    ```

  - Data en un rango de fechas especificas segun Device por POST en el cuerpo opcional [corchetes = opcional]
    - post:
    ```
    data = {'day1': [dia1], 'day2': [dia2],  'month1': [mes1], 'month2': [mes2], 'year1': [year1], 'year2': [year2], 'device_id': [pk]'}
    r = requests.post("http://localhost:8000/data/days", data)
    r.text
    r.url
    ```

  - Data en un rango de fechas y horas especificas segun Device por POST en el cuerpo opcional [corchetes = opcional]
    - post:
    ```
    data = {'hour1': hour1, 'hour2': hour2, 'day1': dia1, 'day2': dia2,  'month1': mes1, 'month2': mes2, 'year1': year1, 'year2': year2, ['device_id']: ['pk']}
    r = requests.post("http://localhost:8000/data/hours", data)
    r.text
    r.url
    ```

### Tasks:

  - DataTask:
    - Create DataTask:
      - post:
      ```
      data = {'taskstate':'1', 'taskfunction':'1', 'label':'done', 'description':'taks is done', 'owner':'root', 'data_value':'10', 'device_mac':'11:11:11:11','comparator':'1','repeats':'5'}
      r = requests.post("http://localhost:8000/tasks/datatasks/create", data=data)
      r.text
      r.url
      ```

    - Update DataTask:
    ```
    data = {'taskstate':'1', 'taskfunction':'1', 'label':'riego', 'description':'regando', 'owner':'root', 'data_value':79, 'device_mac':'11:11:11:11','comparator':'1','repeats':'5'}
    r = requests.post("http://localhost:8000/tasks/datatasks/<datatask_id>/update", data=data)
    r.text
    r.url
    ```

    - List DataTask:
    ```
    r = requests.get("http://localhost:8000/datatasks/")
    r.text
    r.url
    ```

    - DataTask Detail:
    ```
    r = requests.get("http://localhost:8000/datatasks/<datatask_id>")
    r.text
    r.url
    ```

    - DataTasks de Devices:
    ```
    r = requests.get("http://localhost:8000/tasks/devices/<datatask_id>/datatasks/")
    r.text
    r.url
    ```

    - DateTimeTask:
      - Create DateTimeTask:
        - post:
        ```
        data = {'taskstate':'1', 'taskfunction':'1', 'label':'datetimtask1', 'description':'taks is done', 'owner':'root', 'datetime':"2017-10-10T17:23:47.636", 'device_mac':'11:11:11:11','repeats':'5','repeat_criteria':'1'}
        r = requests.post("http://localhost:8000/tasks/datetimetasks/create", data=data)
        r.text
        r.url
        ```

    - Update DateTimeTask:
    ```
    data = {'taskstate':'1', 'taskfunction':'1', 'label':'datetimtask2', 'description':'taks is done', 'owner':'root', 'datetime':datetime, 'device_mac':'11:11:11:11','repeats':'5','repeat_criteria':'1'}
    r = requests.post("http://localhost:8000/tasks/datetimetasks/<datetimetask_id>/update", data=data)
    r.text
    r.url
    ```

    - List DateTimeTask:
    ```
    r = requests.get("http://localhost:8000/datetimetasks/")
    r.text
    r.url
    ```

    - DateTimeTask Detail:
    ```
    r = requests.get("http://localhost:8000/datetimetasks/<datetimetask_id>")
    r.text
    r.url
    ```

    - DateTimeTasks de Devices:
    ```
    r = requests.get("http://localhost:8000/tasks/devices/<datetimetask_id>/datetimetasks/")
    r.text
    r.url
    ```

    - RemoveDataTasks:
    ```
    r = requests.get("http://localhost:8000/tasks/datatasks/<datatask_id>/remove")
    r.text
    r.url
    ```

    - RemoveDateTimeTasks:
    ```
    r = requests.get("http://localhost:8000/tasks/datetimetasks/<datetimetask_id>/remove")
    r.text
    r.url

    ```

    - ReadyTasks:
    ```
    r = requests.get("http://localhost:8000/tasks/readytasks")
    r.text
    r.url
    ```

    - DoneTasks:
    ```
    r = requests.get("http://localhost:8000/tasks/donetasks")
    r.text
    r.url
    ```

    - ReadyDateTimeTasks:
    ```
    r = requests.get("http://localhost:8000/tasks/readydatetimetasks")
    r.text
    r.url
    ```

    - DoneDateTimeTasks:
    ```
    r = requests.get("http://localhost:8000/tasks/donedatetimetasks")
    r.text
    r.url
    ```

    - ReadyDataTasks:
    ```
    r = requests.get("http://localhost:8000/tasks/readydatatasks")
    r.text
    r.url
    ```

    - DoneDataTasks:
    ```
    r = requests.get("http://localhost:8000/tasks/donedatatasks")
    r.text
    r.url
    ```

    - DoneDataTasks:
    ```
    r = requests.get("http://localhost:8000/tasks/donedatatasks")
    r.text
    r.url
    ```

    ## TaskState
      - List taskstates (GET)
      ```
      r = requests.get("http://localhost:8000/tasks/taskstates")
      r.text
      r.url
      ```
