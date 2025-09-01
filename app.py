import streamlit as st
import pandas as pd
import os
from datetime import datetime
import urllib.parse

# ----------------------------
# Configuración de la página
# ----------------------------
st.set_page_config(
    page_title="Formulario Psicomotriz",
    layout="centered"
)

# ----------------------------
# Carpeta y archivo para guardar datos
# ----------------------------
DATA_FOLDER = "datos_guardados"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

DATA_FILE = os.path.join(DATA_FOLDER, "profesionales.csv")

# ----------------------------
# Título principal
# ----------------------------
st.title("Formulario Psicomotriz - Prototipo Web")

# ----------------------------
# Número de WhatsApp de destino (ejemplo)
# ----------------------------
WHATSAPP_NUMBER = "59899999999"  # reemplazá con el número real

# ----------------------------
# Crear pestañas
# ----------------------------
tab1, tab2 = st.tabs(["Resumen", "Formulario"])

# ----------------------------
# Pestaña Resumen
# ----------------------------
with tab1:
    st.header("Resumen")
    st.write("""
    Estimado profesional:
    
    Este enlace que recibiste por WhatsApp te lleva a un **prototipo de formulario web** 
    diseñado para digitalizar los procesos actuales de evaluación en nuestra clínica psicomotriz.  
    
    **Objetivo:**
    - Validar la idea de digitalizar los formularios de evaluación.
    - Mejorar la eficiencia y precisión en la recolección de datos.
    - Facilitar el seguimiento de la evolución de cada paciente.
    
    **Por qué recibiste este link:**
    - Queremos recopilar información de manera segura y rápida de todos los profesionales que participan en el proceso.
    - Tu colaboración nos permitirá validar el prototipo y presentarlo en ANII.
    
    **Instrucciones:**
    1. Hacé click en la pestaña 'Formulario'.
    2. Completá los campos solicitados.
    3. Los datos se guardarán automáticamente y podrán ser revisados por el equipo autorizado.
    
    Gracias por tu colaboración.
    """)

# ----------------------------
# Pestaña Formulario
# ----------------------------
with tab2:
    st.header("Formulario")
    
    # Campos básicos del profesional
    nombre = st.text_input("Nombre completo")
    profesion = st.text_input("Profesión")
    cedula = st.text_input("Cédula")
    
    # Botón para enviar
    if st.button("Enviar"):
        if nombre and profesion and cedula:
            # Guardar datos en CSV
            nueva_fila = pd.DataFrame({
                "Nombre": [nombre],
                "Profesión": [profesion],
                "Cédula": [cedula],
                "Fecha": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            })
            
            if os.path.exists(DATA_FILE):
                df = pd.read_csv(DATA_FILE)
                df = pd.concat([df, nueva_fila], ignore_index=True)
            else:
                df = nueva_fila
            
            df.to_csv(DATA_FILE, index=False)
            
            st.success(f"Gracias {nombre}, tus datos fueron registrados correctamente.")
            
            # Generar link de WhatsApp con los datos
            mensaje = f"Nombre: {nombre}%0AProfesión: {profesion}%0ACédula: {cedula}"
            whatsapp_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={mensaje}"
            
            st.markdown(f"[Enviar datos por WhatsApp]({whatsapp_url})", unsafe_allow_html=True)
        else:
            st.error("Por favor completá todos los campos antes de enviar.")

