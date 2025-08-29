import streamlit as st
import pandas as pd
import os

# Nombre del archivo CSV
FILE_NAME = "evaluaciones.csv"

# Función para guardar los datos
def save_data(data):
    if os.path.exists(FILE_NAME):
        df = pd.read_csv(FILE_NAME)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])
    df.to_csv(FILE_NAME, index=False)

# Título de la app
st.title("📋 Evaluación Psicomotriz")

# Menú lateral
menu = st.sidebar.radio("Navegar", ["Datos del paciente", "Antecedentes", "Prueba Koppitz", "Observaciones", "Guardar evaluación"])

# Diccionario temporal para almacenar los datos
if "form_data" not in st.session_state:
    st.session_state.form_data = {}

# Secciones
if menu == "Datos del paciente":
    st.header("🧍 Datos del paciente")
    st.session_state.form_data["nombre"] = st.text_input("Nombre completo")
    st.session_state.form_data["edad"] = st.number_input("Edad", min_value=0, max_value=100, step=1)
    st.session_state.form_data["sexo"] = st.selectbox("Sexo", ["", "Masculino", "Femenino", "Otro"])
    st.session_state.form_data["derivado"] = st.text_input("Derivado de (si corresponde)")

elif menu == "Antecedentes":
    st.header("📑 Antecedentes")
    st.session_state.form_data["antecedentes_generales"] = st.text_area("Antecedentes generales")
    st.session_state.form_data["evaluaciones_previas"] = st.text_area("Evaluaciones previas / Tests anteriores")

elif menu == "Prueba Koppitz":
    st.header("📝 Test de Koppitz")
    st.session_state.form_data["puntaje_koppitz"] = st.slider("Puntaje obtenido", 0, 10, 5)
    st.session_state.form_data["interpretacion_koppitz"] = st.text_area("Interpretación cualitativa")

elif menu == "Observaciones":
    st.header("👀 Observaciones")
    st.session_state.form_data["observaciones"] = st.text_area("Observaciones adicionales")

elif menu == "Guardar evaluación":
    st.header("💾 Guardar evaluación")
    st.write("Revisar los datos antes de guardar:")
    st.json(st.session_state.form_data)

    if st.button("Guardar en CSV"):
        if st.session_state.form_data.get("nombre"):
            save_data(st.session_state.form_data)
            st.success("✅ Datos guardados en evaluaciones.csv")
            st.session_state.form_data = {}
        else:
            st.error("⚠️ Falta ingresar al menos el nombre del paciente.")
