import requests
result = requests.get("http://localhost:8000/devices/data", data={"device_mac":"33:33:22:22"})
