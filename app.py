import streamlit as st
import pandas as pd
import os
from datetime import datetime
import csv
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
    diseñado para **digitalizar los procesos actuales de evaluación y seguimiento de procesos en la clínica psicomotriz**.

    **Objetivo:**
    - Validar la digitalización de formularios.
    - Mejorar eficiencia y precisión.
    - Facilitar seguimiento de evolución de pacientes.

    **Por qué recibiste este link:**
    - Queremos recopilar información segura de los profesionales que participan.
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

# ----------------------------
# Pestaña 3: Datos del paciente (TABLA EDITABLE)
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
            st.write("Tests seleccionados:", seleccionados)
            st.write("Resultados detallados:", resultados)

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
    st.header("✅ Cuestionario de validación de formulario digital")
    with st.form("form_feedback"):
        usabilidad = st.radio("¿Le resulta fácil de usar este formulario digital?", ["Sí", "Parcialmente", "No"])
        flujo = st.radio("¿Se entiende claramente el flujo de ingreso de información?", ["Sí", "Parcialmente", "No"])
        dificultades = st.text_area("¿Qué dificultades encontró al completar los campos? (respuesta abierta)")
        utilidad = st.radio("¿Este formulario digital le facilitaría su trabajo comparado con el método actual?", ["Mucho", "Algo", "Nada"])
        campos_utiles = st.text_area("¿Qué campos considera más útiles para su labor diaria?")
        mejoras = st.text_area("¿Qué agregarían o modificarían en las secciones existentes?")
        recomendar = st.slider("En una escala del 1 al 5, ¿recomendaría este formulario digital a colegas?", 1, 5)
        otros = st.text_area("Otros comentarios o sugerencias")

        submitted_feedback = st.form_submit_button("Enviar feedback")

        if submitted_feedback:
            st.warning("""
    **IMPORTANTE:** El botón de WhatsApp detecta si estás en PC o móvil. Si tienes WhatsApp Desktop instalado, el mensaje puede no prellenarse automáticamente. Usa WhatsApp Web o la app móvil para mejor experiencia.
    """)

            resumen_compacto = (
                f"Feedback Formulario\n"
                f"Usabilidad: {usabilidad}\n"
                f"Flujo: {flujo}\n"
                f"Dificultades: {dificultades}\n"
                f"Utilidad: {utilidad}\n"
                f"Campos utiles: {campos_utiles}\n"
                f"Mejoras: {mejoras}\n"
                f"Recomendar: {recomendar}\n"
                f"Otros: {otros}"
            )

            st.markdown('<h4>Resumen generado:</h4>', unsafe_allow_html=True)
            st.code(resumen_compacto, language=None)
            
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

            mensaje_codificado = urllib.parse.quote_plus(resumen_compacto)
            numero = "59898776605"

            # JavaScript para detectar dispositivo y abrir el link correcto
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