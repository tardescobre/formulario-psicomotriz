import streamlit as st

# ----------------------------
# Página principal / Título
# ----------------------------
st.set_page_config(
    page_title="Formulario Psicomotriz",
    layout="centered"
)

# ----------------------------
# Título principal
# ----------------------------
st.title("Datos necesarios en la clínica Psicomotriz")

# ----------------------------
# Formulario de Datos del Paciente
# ----------------------------
with st.form("datos_paciente"):
    st.header("Información del paciente")
    
    nombre = st.text_input("Nombre completo")
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])
    fecha = st.date_input("Fecha de evaluación")
    
    # Otros campos que quieras agregar
    observaciones = st.text_area("Observaciones adicionales")
    
    submitted = st.form_submit_button("Guardar datos")
    
    if submitted:
        st.success(f"Datos de {nombre} guardados correctamente.")

# ----------------------------
# Otra sección opcional
# ----------------------------
st.header("Evaluaciones psicomotrices")
st.write("Aquí se pueden agregar más campos de evaluación según corresponda.")



