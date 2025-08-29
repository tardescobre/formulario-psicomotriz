import json
from pathlib import Path

DB_FILE = Path(__file__).parent.parent / "evaluaciones.json"

def cargar_evaluaciones():
    if DB_FILE.exists():
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def guardar_evaluacion(data):
    evaluaciones = cargar_evaluaciones()
    evaluaciones.append(data)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(evaluaciones, f, ensure_ascii=False, indent=4)

# Para probar rápidamente:
if __name__ == "__main__":
    print("Cargando evaluaciones actuales:")
    print(cargar_evaluaciones())
    print("Guardando evaluación de prueba...")
    guardar_evaluacion({"nombre": "Test", "puntaje": 100})
    print("Evaluaciones actualizadas:")
    print(cargar_evaluaciones())
