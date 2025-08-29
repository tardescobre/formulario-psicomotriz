import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Prototipo Formulario", layout="wide")

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "registros.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if "current_record" not in st.session_state:
    st.session_state.current_record = {
        "ingreso": {},
        "evaluacion": {},
        "cuestionario": {},
        "seguimiento": []
    }

@st.cache_data
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame()

def save_record(record):
    seguimiento_text = " || ".join([
        f"[{n['fecha']}] {n['nota']} (áreas: {n.get('areas','')})"
        for n in record.get('seguimiento', [])
    ])
    flat = {
        "timestamp": datetime.datetime.now().isoformat(),
        "nombre": record['ingreso'].get('nombre',''),
        "documento": record['ingreso'].get('documento',''),
        "edad": record['ingreso'].get('edad',''),
        "sexo": record['ingreso'].get('sexo',''),
        "derivado": record['ingreso'].get('derivado',''),
        "fuente_derivacion": record['ingreso'].get('fuente_derivacion',''),
        "motivo_consulta": record['ingreso'].get('motivo',''),
        "antecedentes": record['evaluacion'].get('antecedentes',''),
        "pruebas_previas": record['evaluacion'].get('pruebas_previas',''),
        "observaciones_psicomot": record['evaluacion'].get('observaciones',''),
        "cuestionario_resumen": str(record['cuestionario']),
        "seguimiento": seguimiento_text
    }
    df = load_data()
    df = pd.concat([df, pd.DataFrame([flat])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# -------- UI --------
menu = st.sidebar.radio("Menú", [
    "Ingreso",
    "Evaluación inicial",
    "Cuestionario padres/docentes",
    "Seguimiento",
    "📑 Ver registros"
])

if menu == "Ingreso":
    st.header("📌 Ingreso del paciente")
    nombre = st.text_input("Nombre completo")
    documento = st.text_input("Documento")
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    sexo = st.selectbox("Sexo", ["", "Masculino", "Femenino", "Otro"])
    derivado = st.radio("¿Viene derivado?", ["Sí", "No"])
    fuente = ""
    if derivado == "Sí":
        fuente = st.text_input("Fuente de derivación (ej: escuela, pediatra)")
    motivo = st.text_area("Motivo de consulta")
    if st.button("Guardar ingreso"):
        st.session_state.current_record["ingreso"] = {
            "nombre": nombre,
            "documento": documento,
            "edad": edad,
            "sexo": sexo,
            "derivado": derivado,
            "fuente_derivacion": fuente,
            "motivo": motivo
        }
        st.success("Ingreso guardado en memoria ✔️")

elif menu == "Evaluación inicial":
    st.header("📝 Evaluación inicial")
    antecedentes = st.text_area("Antecedentes generales")
    pruebas = st.text_area("Pruebas previas realizadas")
    observaciones = st.text_area("Observaciones psicomotrices")
    if st.button("Guardar evaluación"):
        st.session_state.current_record["evaluacion"] = {
            "antecedentes": antecedentes,
            "pruebas_previas": pruebas,
            "observaciones": observaciones
        }
        st.success("Evaluación guardada en memoria ✔️")

elif menu == "Cuestionario padres/docentes":
    st.header("📋 Cuestionario")
    atencion = st.slider("Atención observada", 1, 10, 5)
    motricidad = st.slider("Motricidad observada", 1, 10, 5)
    observaciones = st.text_area("Observaciones adicionales")
    if st.button("Guardar cuestionario"):
        st.session_state.current_record["cuestionario"] = {
            "atencion": atencion,
            "motricidad": motricidad,
            "observaciones": observaciones
        }
        st.success("Cuestionario guardado en memoria ✔️")

elif menu == "Seguimiento":
    st.header("🔎 Seguimiento")
    nota = st.text_area("Nueva nota de seguimiento")
    areas = st.text_input("Áreas involucradas (separadas por coma)")
    if st.button("Agregar nota"):
        st.session_state.current_record["seguimiento"].append({
            "fecha": datetime.date.today().isoformat(),
            "nota": nota,
            "areas": areas
        })
        st.success("Nota añadida al seguimiento ✔️")
    st.subheader("Notas guardadas:")
    for n in st.session_state.current_record["seguimiento"]:
        st.write(f"- [{n['fecha']}] {n['nota']} ({n.get('areas','')})")

elif menu == "📑 Ver registros":
    st.header("📑 Registros guardados en CSV")
    df = load_data()
    st.dataframe(df)
    if st.button("💾 Guardar registro actual en CSV"):
        save_record(st.session_state.current_record)
        st.success("Registro completo guardado en registros.csv ✔️")
