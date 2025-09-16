import pandas as pd
import csv
import os

# Detectar el separador de feedback1.csv
with open('feedback1.csv', 'r', encoding='utf-8', newline='') as f:
    first_line = f.readline()
    if ';' in first_line:
        sep = ';'
    elif '\t' in first_line:
        sep = '\t'
    elif ',' in first_line:
        sep = ','
    else:
        sep = ','  # Por defecto

# Leer el archivo con el separador detectado
try:
    df = pd.read_csv('feedback1.csv', sep=sep, encoding='utf-8', engine='python')
except Exception:
    # Si falla, intenta con cp1252
    df = pd.read_csv('feedback1.csv', sep=sep, encoding='cp1252', engine='python')

# Si los datos están todos en una sola columna, intenta separarlos
if df.shape[1] == 1:
    # Intenta dividir por coma
    df = df[df.columns[0]].str.split(',', expand=True)

# Asignar nombres de columna igual que feedback2.csv (ajusta si tu CSV2 tiene otros nombres)
df.columns = [
    "nombre_profesional", "cedula_profesional", "profesion_profesional",
    "utilidad", "utilidad_opcion", "eficiencia", "eficiencia_opcion",
    "intencion_uso", "satisfaccion_claridad", "satisfaccion_claridad_opcion",
    "satisfaccion_diseño", "satisfaccion_diseño_opcion",
    "modificar_secciones", "comentarios", "fecha_envio"
]

# Limpiar espacios
for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

# Guardar el CSV normalizado
df.to_csv('feedback1_normalizado.csv', index=False, encoding='utf-8-sig')
print("CSV1 normalizado y listo para análisis: feedback1_normalizado.csv")
