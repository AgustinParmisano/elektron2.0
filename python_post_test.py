import requests
result = requests.post("http://localhost:8000/devices/data", data={"device_mac":"12:12:12:12"})
print result.content
