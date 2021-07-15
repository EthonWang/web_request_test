
import requests

response = requests.get("https://geomodeling.njnu.edu.cn/")
print(type(response.status_code))
print(response.status_code)