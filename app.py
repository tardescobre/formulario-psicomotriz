import streamlit as st
import pandas as pd
from datetime import date
import os

# ----------------------------
# Configuración de la página
# ----------------------------
st.set_page_config(
    page_title="Formulario Psicomotriz",
    layout="centered"
)

# ----------------------------
# Carpeta para guardar los datos
# ----------------------------
DATA_FOLDER = "datos_guardados"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# ----------------------------
# Pestañas / páginas
# ----------------------------
tabs = st.tabs(["Lista", "Datos Paciente", "Antecedentes", "Tests", "Seguimiento del proceso", "Guardar evaluación", "Cuestionario de validación"])

# ----------------------------
# 0️⃣ Lista de pacientes editable
# ----------------------------
with tabs[0]:
    st.title("Lista de pacientes")
    
    # Crear DataFrame vacío al inicio si no existe
    if "df_lista" not in st.session_state:
        st.session_state.df_lista = pd.DataFrame(columns=["Nombre", "Día", "Hora"])
    
    # Mostrar tabla editable
    st.session_state.df_lista = st.data_editor(
        st.session_state.df_lista,
        num_rows="dynamic",
        use_container_width=True
    )
    
    st.info("Agrega los pacientes con su nombre, día y hora de consulta. Los cambios se pueden editar en esta tabla.")

# ----------------------------
# 1️⃣ Datos del Paciente
# ----------------------------
with tabs[1]:
    st.title("Datos necesarios en la clínica Psicomotriz")
    
    with st.form("form_paciente"):
        nombre = st.text_input("Nombre completo")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
        sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])
        fecha = st.date_input("Fecha de evaluación", value=date.today())
        observaciones_iniciales = st.text_area("Observaciones iniciales")
        
        submitted_paciente = st.form_submit_button("Guardar datos del paciente")
        
        if submitted_paciente:
            paciente_data = {
                "Nombre": nombre,
                "Edad": edad,
                "Sexo": sexo,
                "Fecha": fecha,
                "Observaciones iniciales": observaciones_iniciales
            }
            df_paciente = pd.DataFrame([paciente_data])
            df_paciente.to_csv(os.path.join(DATA_FOLDER, f"paciente_{nombre}_{fecha}.csv"), index=False)
            st.success(f"Datos de {nombre} guardados correctamente.")

# ----------------------------
# 2️⃣ Antecedentes
# ----------------------------
with tabs[2]:
    st.header("Antecedentes")
    with st.form("form_antecedentes"):
        antecedentes = st.text_area("Ingrese los antecedentes del paciente")
        derivado = st.radio("¿Fue derivado?", ["Sí", "No"])
        if derivado == "Sí":
            origen = st.text_input("Origen de la derivación")
        else:
            origen = ""
        
        submitted_antec = st.form_submit_button("Guardar antecedentes")
        if submitted_antec:
            st.success("Antecedentes guardados correctamente!")
            st.write("Antecedentes:", antecedentes)
            st.write("Derivado:", derivado)
            if derivado == "Sí":
                st.write("Origen de la derivación:", origen)

# ----------------------------
# 3️⃣ Tests psicomotrices
# ----------------------------
with tabs[3]:
    st.header("Tests psicomotrices")
    
    tests_disponibles = [
        "DFH Koppitz",
        "Reversal Test",
        "Test de Figura Compleja",
        "Test escritura Ajuriaguerra",
        "Test de Bender",
        "Esquema Corporal Vitor Da Fonseca",
        "Batería Piaget-Head",
        "Test de Dibujo Libre",
        "Test de Frostig",
        "Test de Pascual"
    ]
    
    with st.form("form_tests"):
        seleccionados = st.multiselect("Seleccione los tests realizados", tests_disponibles)
        resultados = st.text_area("Detalle los resultados de los tests")
        submitted_tests = st.form_submit_button("Guardar tests")
        
        if submitted_tests:
            st.success("Tests guardados correctamente!")
            st.write("Tests seleccionados:", seleccionados)
            st.write("Resultados detallados:", resultados)

# ----------------------------
# 4️⃣ Seguimiento del proceso
# ----------------------------
with tabs[4]:
    st.header("Seguimiento del proceso")
    
    with st.form("form_seguimiento"):
        st.subheader("Notas de relevancia clínica")
        notas_clinicas = st.text_area("")  # Solo título arriba, texto libre aquí
        
        st.subheader("Ideas cualitativas sobre el proceso vincular")
        ideas_vinculares = st.text_area(
            "Cómo se van construyendo las relaciones niño–familia–escuela–terapeuta"
        )
        
        st.subheader("Observaciones / Avances")
        motor = st.text_area("Motor")
        afectivo = st.text_area("Afectivo")
        relacional = st.text_area("Relacional")
        cognitivo = st.text_area("Cognitivo")
        
        submitted_seguimiento = st.form_submit_button("Guardar seguimiento")
        if submitted_seguimiento:
            st.success("Seguimiento registrado correctamente!")
            st.write("Notas clínicas:", notas_clinicas)
            st.write("Ideas vinculares:", ideas_vinculares)
            st.write("Observaciones / Avances:")
            st.write("Motor:", motor)
            st.write("Afectivo:", afectivo)
            st.write("Relacional:", relacional)
            st.write("Cognitivo:", cognitivo)

# ----------------------------
# 5️⃣ Guardar evaluación
# ----------------------------
with tabs[5]:
    st.header("Guardar evaluación completa")
    with st.form("form_guardar"):
        comentario_final = st.text_area("Comentarios finales antes de guardar evaluación")
        submitted_final = st.form_submit_button("Guardar evaluación")
        if submitted_final:
            st.success("Evaluación completa guardada correctamente!")

# 6️⃣ Cuestionario de validación
# ----------------------------
with tabs[6]:
    st.header("Cuestionario de validación de formulario digital")
    with st.form("form_validacion"):
        st.subheader("1️⃣ Usabilidad / Experiencia de usuario")
        facil_uso = st.radio("¿Le resulta fácil de usar este formulario digital?", ["Sí", "Parcialmente", "No"])
        flujo_claro = st.radio("¿Se entiende claramente el flujo de ingreso de información?", ["Sí", "Parcialmente", "No"])
        dificultades = st.text_area("¿Qué dificultades encontró al completar los campos?")

        st.subheader("2️⃣ Utilidad profesional")
        utilidad = st.radio("¿Este formulario digital le facilitaría su trabajo comparado con el método actual (papel)?", ["Mucho", "Algo", "Nada"])
        campos_utiles = st.text_area("¿Qué campos considera más útiles para su labor diaria?")
        faltan_datos = st.text_area("¿Faltan datos importantes que normalmente recogen de otra manera?")

        st.subheader("3️⃣ Mejoras al formulario")
        mejoras = st.text_area("¿Qué agregarían o modificarían en las secciones existentes? (Datos del paciente, Antecedentes, Prueba Koppitz, Observaciones)")
        orden = st.text_area("¿Cambiarían el orden de los campos para que sea más lógico?")
        alertas = st.text_area("¿Agregarían algún tipo de alerta, nota o comentario para pacientes específicos?")

        st.subheader("4️⃣ Retroalimentación general")
        gusto = st.text_area("¿Qué le gustó del formulario?")
        cambios = st.text_area("¿Qué cambiaría para que sea más eficiente o confiable?")
        recomendacion = st.slider("En una escala del 1 al 5, ¿recomendaría este formulario digital a colegas?", 1, 5, 3)
        otros = st.text_area("Otros comentarios o sugerencias:")

        submitted_validacion = st.form_submit_button("Enviar feedback")
        if submitted_validacion:
            st.success("¡Gracias por tu feedback! Tus respuestas han sido registradas.")



