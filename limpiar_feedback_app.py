
import pandas as pd
import os

# Ruta del archivo original y el archivo limpio
input_file = os.path.join('datos_guardados', 'feedback_app.csv')
output_file = os.path.join('datos_guardados', 'feedback_app_limpio.csv')

# Leer el archivo original
df = pd.read_csv(input_file, encoding='utf-8-sig')

# Seleccionar solo las columnas relevantes (una por pregunta, sin duplicados conceptuales)
columnas_deseadas = [
    'nombre_profesional',
    'utilidad',
    'eficiencia',
    'intencion_uso',
    'satisfaccion_claridad',
    'satisfaccion_diseño',
    'modificar_secciones',
    'comentarios',
    'fecha_envio',
    'cedula_profesional',
    'profesion_profesional'
]

# Filtrar solo las columnas que existen en el archivo
columnas_finales = [col for col in columnas_deseadas if col in df.columns]
df_limpio = df[columnas_finales].copy()


# Eliminar filas con datos obligatorios vacíos o nulos
obligatorias = ["nombre_profesional", "utilidad", "eficiencia", "intencion_uso", "satisfaccion_claridad", "satisfaccion_diseño"]
for col in obligatorias:
    df_limpio = df_limpio[df_limpio[col].astype(str).str.strip() != ""]
    df_limpio = df_limpio[df_limpio[col].notna()]


# No eliminar duplicados, mantener todos los registros completos

# Guardar el archivo limpio con todos los registros
df_limpio.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"Archivo limpio guardado en: {output_file}")
