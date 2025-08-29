import requests

data = {"nombre": "Juan", "puntaje": 12}
url = "https://tankerale.pythonanywhere.com/api/evaluacion"

response = requests.post(url, json=data)
print("Código de respuesta:", response.status_code)
print("Respuesta JSON:", response.json())

