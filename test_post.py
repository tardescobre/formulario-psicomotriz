import requests

data = {"nombre": "Diego", "puntaje": 10}
resp = requests.post("http://127.0.0.1:5000/api/evaluacion", json=data)

print("Código de respuesta:", resp.status_code)
try:
    print("Respuesta JSON:", resp.json())
except Exception:
    print("Respuesta en texto:", resp.text)
