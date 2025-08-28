from flask import Flask, request, jsonify, render_template_string
import json
from pathlib import Path

app = Flask(__name__)

# Ruta al archivo JSON en la misma carpeta que server.py
DB_PATH = Path(__file__).parent / "evaluaciones.json"

# Función para cargar evaluaciones
def cargar_evaluaciones():
    if DB_PATH.exists():
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# Inicializamos la lista de evaluaciones
evaluaciones = cargar_evaluaciones()

# -----------------------
# Formulario web
# -----------------------
@app.route('/', methods=['GET', 'POST'])
def formulario():
    global evaluaciones
    mensaje = ""
    if request.method == 'POST':
        nombre = request.form.get("nombre", "").strip()
        try:
            coordinacion = int(request.form.get("coordinacion", 0))
        except:
            coordinacion = 0
        try:
            equilibrio = int(request.form.get("equilibrio", 0))
        except:
            equilibrio = 0
        try:
            atencion = int(request.form.get("atencion", 0))
        except:
            atencion = 0

        if nombre:
            evaluaciones.append({
                "nombre": nombre,
                "puntajes": {
                    "coordinacion": coordinacion,
                    "equilibrio": equilibrio,
                    "atencion": atencion
                }
            })
            # Guardar en JSON
            with open(DB_PATH, "w", encoding="utf-8") as f:
                json.dump(evaluaciones, f, ensure_ascii=False, indent=4)
            mensaje = "✅ Guardado correctamente. <a href='/resultados_web'>Ver resultados</a>"
        else:
            mensaje = "⚠️ Debes ingresar un nombre"

    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Formulario Evaluación</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f4f4f4; }
            form { background: white; padding: 20px; max-width: 400px; margin: auto; border-radius: 10px; box-shadow: 0 0 10px #aaa; }
            label { display: block; margin-top: 10px; }
            input[type=text], input[type=number] { width: 100%; padding: 8px; margin-top: 5px; }
            button { margin-top: 15px; padding: 10px; width: 100%; background: #4CAF50; color: white; border: none; border-radius: 5px; }
            p { text-align: center; color: green; }
        </style>
    </head>
    <body>
        <form method="POST">
            <h2>Formulario de Evaluación</h2>
            <label>Nombre del paciente:</label>
            <input type="text" name="nombre" required>
            
            <label>Coordinación (0-10):</label>
            <input type="number" name="coordinacion" min="0" max="10" required>
            
            <label>Equilibrio (0-10):</label>
            <input type="number" name="equilibrio" min="0" max="10" required>
            
            <label>Atención (0-10):</label>
            <input type="number" name="atencion" min="0" max="10" required>
            
            <button type="submit">Guardar Evaluación</button>
            {% if mensaje %}
            <p>{{ mensaje|safe }}</p>
            {% endif %}
        </form>
    </body>
    </html>
    """
    return render_template_string(html, mensaje=mensaje)

# -----------------------
# Página de resultados
# -----------------------
@app.route('/resultados_web', methods=['GET'])
def resultados_web():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Resultados Evaluaciones</title>
        <style>
            table { border-collapse: collapse; width: 70%; margin: 20px auto; }
            th, td { border: 1px solid #333; padding: 8px; text-align: center; }
            th { background-color: #f2f2f2; }
            h2 { text-align: center; }
        </style>
    </head>
    <body>
        <h2>Resultados de Evaluaciones Psicomotrices</h2>
        <table>
            <tr>
                <th>#</th>
                <th>Paciente</th>
                <th>Coordinación</th>
                <th>Equilibrio</th>
                <th>Atención</th>
            </tr>
            {% for eval in evaluaciones %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ eval.get('nombre', 'Sin nombre') }}</td>
                <td>{{ eval.get('puntajes', {}).get('coordinacion', 0) }}</td>
                <td>{{ eval.get('puntajes', {}).get('equilibrio', 0) }}</td>
                <td>{{ eval.get('puntajes', {}).get('atencion', 0) }}</td>
            </tr>
            {% endfor %}
        </table>
        <p style="text-align:center;"><a href="/">← Volver al formulario</a></p>
    </body>
    </html>
    """
    return render_template_string(html, evaluaciones=evaluaciones)

# -----------------------
# Endpoint para app Kivy
# -----------------------
@app.route('/api/guardar_datos', methods=['POST'])
def api_guardar_datos():
    global evaluaciones
    data = request.get_json()
    nombre = data.get("nombre")
    puntajes = data.get("puntajes", {})
    if not nombre:
        return jsonify({"error":"Falta nombre"}), 400
    for key in ["coordinacion","equilibrio","atencion"]:
        puntajes.setdefault(key,0)
    evaluaciones.append({"nombre":nombre,"puntajes":puntajes})
    with open(DB_PATH,"w",encoding="utf-8") as f:
        json.dump(evaluaciones,f,ensure_ascii=False,indent=4)
    return jsonify({"message":"Guardado correctamente"}), 200

# -----------------------
# Ejecutar servidor
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
