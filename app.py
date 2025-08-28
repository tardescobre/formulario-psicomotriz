# app.py (Flask)
from flask import Flask, request, jsonify

app = Flask(__name__)
pacientes = []

@app.route('/api/guardar_datos', methods=['POST'])
def guardar_datos():
    data = request.get_json()
    pacientes.append(data)
    return jsonify({"status": "ok", "total": len(pacientes)})

@app.route('/api/listar', methods=['GET'])
def listar():
    return jsonify(pacientes)

if __name__ == '__main__':
    app.run(debug=True)
