import streamlit as st
import pandas as pd
import os
from datetime import datetime
import urllib.parse
import streamlit.components.v1 as components

# ----------------------------
# Configuración de la página
# ----------------------------
st.set_page_config(
    page_title="Formulario Psicomotriz",
    layout="centered"
)

# ----------------------------
# Carpetas y archivos
# ----------------------------
DATA_FOLDER = "datos_guardados"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

DATA_FILE_PROF = os.path.join(DATA_FOLDER, "profesionales.csv")
PACIENTES_FILE = os.path.join(DATA_FOLDER, "pacientes.csv")

# ----------------------------
# Definición de pestañas
# ----------------------------
tabs = st.tabs([
    "Introducción",
    "Registro de datos del profesional",
    "Datos del paciente",
    "Antecedentes",
    "Tests psicomotrices",
    "Seguimiento del proceso",
    "Guardar evaluación",
    "Lista de pacientes",
    "Cuestionario de validación"
])

# ----------------------------
# Pestaña 1: Introducción
# ----------------------------
with tabs[0]:
    st.title("Formulario Psicomotriz - Prototipo Web")
    
    # Presentación del equipo
    st.markdown("""
    **Equipo responsable del proyecto:**  
    - 👩‍⚕️ Licenciada en Psicomotricidad  
    - 📊 Licenciado en Estadística
    """)
    
    st.header("Resumen")
    st.write("""
    Estimado profesional:

    Este enlace que recibiste por WhatsApp te lleva a un **prototipo de formulario web** 
    diseñado para **digitalizar los procesos de evaluación y seguimiento de los pacientes en la clínica psicomotriz**.
             
    Si tu profesión es otra y recibiste el link, es porque consideramos que tus aportes serán fundamentales para este proyecto y la posibilidad de ampliarlo hacia otras disciplinas en un futuro.

    **Objetivo:**
    - Validar la digitalización de formularios.
    - Mejorar eficiencia y precisión.
    - Facilitar seguimiento de evolución de pacientes.

    **¿Por qué recibiste este link?**
    - Queremos recopilar información de los profesionales que participan.
    - Tu colaboración permitirá validar el prototipo para realizar una investigación.
    """)

# ----------------------------
# Pestaña 2: Registro de datos del profesional
# ----------------------------
with tabs[1]:
    st.header("Registro de datos del profesional")
    
    nombre_prof = st.text_input("Nombre completo", key="prof_nombre")
    profesion_prof = st.text_input("Profesión", key="prof_profesion")
    cedula_prof = st.text_input("Cédula", key="prof_cedula")

    if st.button("Registrar datos profesionales"):
        if nombre_prof and profesion_prof and cedula_prof:
            # Guardar datos profesionales en CSV
            nueva_fila = pd.DataFrame({
                "Nombre": [nombre_prof],
                "Profesión": [profesion_prof],
                "Cédula": [cedula_prof],
                "Fecha registro": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            })
            if os.path.exists(DATA_FILE_PROF):
                df = pd.read_csv(DATA_FILE_PROF)
                df = pd.concat([df, nueva_fila], ignore_index=True)
            else:
                df = nueva_fila
            df.to_csv(DATA_FILE_PROF, index=False)
            st.success(f"Gracias {nombre_prof}, tus datos fueron registrados correctamente.")
        else:
            st.error("Por favor completá todos los campos del profesional.")
            # Mensaje al pie de la página, debajo de todo
st.markdown("<div style='margin-top:50px; color:gray;'>En la pestaña siguiente comienza el prototipo de formulario para cada paciente.</div>", unsafe_allow_html=True)

# ----------------------------
# Pestaña 3: Datos del paciente
# ----------------------------
with tabs[2]:
    st.header("Datos del paciente")
    
    # Inicializar dataframe si no existe
    if os.path.exists(PACIENTES_FILE):
        df_pacientes = pd.read_csv(PACIENTES_FILE)
    else:
        df_pacientes = pd.DataFrame(columns=["Nombre", "Fecha", "Hora"])
    
    # Tabla editable de pacientes
    st.subheader("Pacientes registrados (editable)")
    edited_df = st.data_editor(
        df_pacientes,
        num_rows="dynamic",
        use_container_width=True,
        key="pacientes_editor"
    )
    if st.button("Guardar cambios en la tabla"):
        edited_df.to_csv(PACIENTES_FILE, index=False)
        st.success("Cambios guardados correctamente.")

# ----------------------------
# Pestaña 4: Antecedentes
# ----------------------------
with tabs[3]:
    st.header("Antecedentes")
    with st.form("form_antecedentes"):
        antecedentes = st.text_area("Ingrese los antecedentes del paciente")
        derivado_por = st.text_input("Derivado por:")
        origen = st.text_input("Origen de la derivación")
        submitted_antec = st.form_submit_button("Guardar antecedentes")
        if submitted_antec:
            st.success("Antecedentes guardados correctamente!")

# ----------------------------
# Pestaña 5: Tests psicomotrices
# ----------------------------
with tabs[4]:
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

# ----------------------------
# Pestaña 6: Seguimiento del proceso
# ----------------------------
with tabs[5]:
    st.header("Seguimiento del proceso")
    with st.form("form_seguimiento"):
        st.subheader("Notas de relevancia clínica")
        notas_clinicas = st.text_area("")
        st.subheader("Ideas cualitativas sobre el proceso vincular")
        ideas_vinculares = st.text_area("Cómo se van construyendo las relaciones niño–familia–escuela–terapeuta")
        st.subheader("Observaciones / Avances")
        motor = st.text_area("Motor")
        afectivo = st.text_area("Afectivo")
        relacional = st.text_area("Relacional")
        submitted_seguimiento = st.form_submit_button("Guardar seguimiento")
        if submitted_seguimiento:
            st.success("Seguimiento guardado correctamente!")

# ----------------------------
# Pestaña 7: Guardar evaluación
# ----------------------------
with tabs[6]:
    st.header("Guardar evaluación completa")
    with st.form("form_guardar"):
        comentario_final = st.text_area("Comentarios finales antes de guardar evaluación")
        submitted_final = st.form_submit_button("Guardar evaluación")

# ----------------------------
# Pestaña 8: Lista de pacientes
# ----------------------------
with tabs[7]:
    st.header("📋 Lista de pacientes registrados")
    try:
        if os.path.exists(PACIENTES_FILE):
            df_pacientes = pd.read_csv(PACIENTES_FILE)
            st.dataframe(df_pacientes)
        else:
            st.info("No hay pacientes registrados aún.")
    except Exception as e:
        st.info("No hay registros de pacientes aún o el archivo no existe.")

# ----------------------------
# Pestaña 9: Cuestionario de validación
# ----------------------------
with tabs[8]:
    st.header("✅ Cuestionario de validación de la app")

    FEEDBACK_FILE = os.path.join(DATA_FOLDER, "feedback_app.csv")

    with st.form("form_feedback"):
        # Mapas de respuestas cualitativas a numéricas
        utilidad_map = {"Mucho": 5, "Algo": 3, "Nada": 1}
        eficiencia_map = {"Sí": 5, "Parcialmente": 3, "No": 1}
        satisfaccion_map = {"Sí": 5, "Parcialmente": 3, "No": 1}
        diseño_map = {
            "Muy bueno": 5,
            "Bueno": 4,
            "Regular": 3,
            "Malo": 2,
            "Muy malo": 1
        }

        # ------------------
        # Preguntas
        # ------------------
        utilidad_resp = st.radio(
            "¿Este formulario digital le facilitaría su trabajo comparado con el método actual?",
            ["Mucho", "Algo", "Nada"]
        )
        eficiencia_resp = st.radio(
            "¿Cree que este formulario ayuda a que sus procesos sean más eficientes?",
            ["Sí", "Parcialmente", "No"]
        )
        intencion_uso = st.slider(
            "En una escala del 0 al 10, ¿qué probabilidad tiene de usar esta app regularmente?",
            0, 10, 7
        )
        satisfaccion_claridad = st.radio(
            "¿Considera que el formulario es claro y fácil de completar?",
            ["Sí", "Parcialmente", "No"]
        )
        satisfaccion_diseño = st.radio(
            "¿Cómo evalúa el diseño visual de la app?",
            ["Muy bueno", "Bueno", "Regular", "Malo", "Muy malo"]
        )

        mejoras = st.text_area("¿Qué agregarían o modificarían en las secciones existentes?")
        comentarios = st.text_area("Comentarios o sugerencias adicionales (respuesta libre)")

        submitted_feedback = st.form_submit_button("Enviar feedback")

        if submitted_feedback:
            # ------------------
            # Mapear respuestas a valores numéricos
            # ------------------
            utilidad_val = utilidad_map[utilidad_resp]
            eficiencia_val = eficiencia_map[eficiencia_resp]
            satisfaccion_claridad_val = satisfaccion_map[satisfaccion_claridad]
            satisfaccion_diseño_val = diseño_map[satisfaccion_diseño]

            # ------------------
            # Guardar en CSV
            # ------------------
            nueva_fila = pd.DataFrame({
                "utilidad": [utilidad_val],
                "eficiencia": [eficiencia_val],
                "intencion_uso": [intencion_uso],
                "satisfaccion_claridad": [satisfaccion_claridad_val],
                "satisfaccion_diseño": [satisfaccion_diseño_val],
                "mejoras": [mejoras],
                "comentarios": [comentarios],
                "fecha_envio": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            })

            if os.path.exists(FEEDBACK_FILE):
                df_feedback = pd.read_csv(FEEDBACK_FILE)
                df_feedback = pd.concat([df_feedback, nueva_fila], ignore_index=True)
            else:
                df_feedback = nueva_fila
            df_feedback.to_csv(FEEDBACK_FILE, index=False)

            st.success("¡Gracias! Tu feedback fue registrado correctamente.")

            # ------------------
            # Generar resumen para WhatsApp
            # ------------------
            resumen_compacto = (
                f"Feedback App\n"
                f"Utilidad: {utilidad_val}/5\n"
                f"Eficiencia: {eficiencia_val}/5\n"
                f"Intención de uso: {intencion_uso}/10\n"
                f"Satisfacción claridad: {satisfaccion_claridad_val}/5\n"
                f"Satisfacción diseño: {satisfaccion_diseño_val}/5\n"
                f"Mejoras: {mejoras}\n"
                f"Comentarios: {comentarios}"
            )

            st.markdown('<h4>Resumen generado:</h4>', unsafe_allow_html=True)
            st.code(resumen_compacto, language=None)

            # ------------------
            # Botón copiar al portapapeles
            # ------------------
            copy_code = f'''
<button id="copyBtn" style="background-color:#25D366;color:white;padding:1em 2em;font-size:1.2em;border:none;border-radius:8px;font-weight:bold;cursor:pointer;">📋 Copiar feedback</button>
<script>
document.getElementById('copyBtn').onclick = function() {{
    navigator.clipboard.writeText(`{resumen_compacto}`);
    alert('¡Resumen copiado! Ahora pégalo en WhatsApp.');
}}
</script>
'''
            components.html(copy_code, height=80)

            # ------------------
            # Botón enviar WhatsApp
            # ------------------
            mensaje_codificado = urllib.parse.quote_plus(resumen_compacto)
            numero = "59898776605"

            js_code = f'''
<button id="wappBtn" style="background-color:#25D366;color:white;padding:1em 2em;font-size:1.2em;border:none;border-radius:8px;font-weight:bold;cursor:pointer;margin-top:1em;">💬 Enviar feedback por WhatsApp</button>
<script>
document.getElementById('wappBtn').onclick = function() {{
    var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    var url = '';
    if (isMobile) {{
        url = 'https://wa.me/?text={mensaje_codificado}';
    }} else {{
        url = 'https://web.whatsapp.com/send?phone={numero}&text={mensaje_codificado}';
    }}
    window.open(url, '_blank');
}}
</script>
'''
            components.html(js_code, height=120)

