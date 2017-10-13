## Use with python resquests:

```
import requests
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

  - Device devices/<device_id>/turon enviar mensaje de apagado al dispositivo:
  ```
  r = requests.get("http://localhost:8000/devices/<device_id>/turnon")
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

  - Data en un rango de fechas especificas y horas segun Device por POST en el cuerpo opcional [corchetes = opcional]
    - post:
    ```
    data = {'day: [dia], month: [mes], year: [year], device_id: [pk]'}
    r = requests.post("http://localhost:8000/data/date, data")
    r.text
    r.url
    ```


### Tasks:

  - DataTask:
    - Create DataTask:
      - post:
      ```
      data = {'taskstate':'1', 'taskfunction':'1', 'label':'done', 'description':'taks is done', 'owner':'root', 'data_value':'10', 'device_mac':'11:11:11:11'}
      r = requests.post("http://localhost:8000/tasks/datatasks/create", data=data)
      r.text
      r.url
      ```

    - Update DataTask:
    ```
    data = {'taskstate':'1', 'taskfunction':'1', 'label':'riego', 'description':'regando', 'owner':'root', 'data_value':79, 'device_mac':'33:33:22:22'}
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
        data = {'taskstate':'1', 'taskfunction':'1', 'label':'done', 'description':'taks is done', 'owner':'root', 'data_from':datetime, 'data_to':datetime, 'device_mac':'11:11:11:11'}
        r = requests.post("http://localhost:8000/tasks/datetimetasks/create", data=data)
        r.text
        r.url
        ```

    - Update DatTimeTask:
    ```
    data = {'taskstate':'1', 'taskfunction':'1', 'label':'done', 'description':'taks is done', 'owner':'root', 'data_from':datetime, 'data_to':datetime, 'device_mac':'11:11:11:11'}
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
