import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ----------------------------
# Configuración de la página
# ----------------------------
st.set_page_config(page_title="Formulario Psicomotriz", layout="centered")

# ----------------------------
# Carpetas y archivos
# ----------------------------
DATA_FOLDER = "datos_guardados"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

DATA_FILE_PROF = os.path.join(DATA_FOLDER, "profesionales.csv")

# ----------------------------
# Título principal
# ----------------------------
st.title("Formulario Psicomotriz - Prototipo Web")

# ----------------------------
# Sección Resumen
# ----------------------------
st.header("Resumen")
st.write("""
Estimado profesional:

Este enlace que recibiste por WhatsApp te lleva a un **prototipo de formulario web** 
diseñado para digitalizar los procesos actuales de evaluación en nuestra clínica psicomotriz.

**Objetivo:**
- Validar la digitalización de formularios.
- Mejorar eficiencia y precisión.
- Facilitar seguimiento de evolución de pacientes.

**Por qué recibiste este link:**
- Queremos recopilar información segura y rápida de los profesionales que participan.
- Tu colaboración permitirá validar el prototipo para ANII.
""")

# Datos del profesional (solo para registro interno)
nombre = st.text_input("Nombre completo")
profesion = st.text_input("Profesión")
cedula = st.text_input("Cédula")

if st.button("Registrar datos profesionales"):
    if nombre and profesion and cedula:
        # Guardar datos profesionales en CSV
        nueva_fila = pd.DataFrame({
            "Nombre": [nombre],
            "Profesión": [profesion],
            "Cédula": [cedula],
            "Fecha registro": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        })
        if os.path.exists(DATA_FILE_PROF):
            df = pd.read_csv(DATA_FILE_PROF)
            df = pd.concat([df, nueva_fila], ignore_index=True)
        else:
            df = nueva_fila
        df.to_csv(DATA_FILE_PROF, index=False)
        st.success(f"Gracias {nombre}, tus datos fueron registrados correctamente.")
    else:
        st.error("Por favor completá todos los campos del profesional.")



