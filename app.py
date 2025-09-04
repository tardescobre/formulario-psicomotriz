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
FEEDBACK_FILE = os.path.join(DATA_FOLDER, "feedback_app.csv")

# ----------------------------
# Definición de pestañas
# ----------------------------
tabs = st.tabs([
    "Introducción",
    "Registro de datos del profesional",
    "Datos del paciente",
    "Antecedentes",
    "Entrevista inicial",
    "Exploración",
    "Tests psicomotrices",
    "Seguimiento del proceso",
    "Guardar Evaluación Completa",
    "📋 Lista de pacientes registrados",
    "Cuestionario de validación"
])

# ----------------------------
# Pestaña 1: Introducción
# ----------------------------
with tabs[0]:
    # Título principal
    st.markdown("<h1 style='text-align: center;'>Formulario Psicomotriz - Prototipo Web</h1>", unsafe_allow_html=True)

    # Texto introductorio
    st.markdown("""
    ### Resumen

    Estimado/a profesional:

    El enlace que recibiste por WhatsApp te dirige a un prototipo de formulario web diseñado para digitalizar los procesos de evaluación y seguimiento en la clínica psicomotriz.

    **Objetivos principales:**
    - Validar la digitalización de formularios.
    - Mejorar la eficiencia y precisión.
    - Facilitar el seguimiento de la evolución de pacientes.

    **¿Por qué recibiste este link?**
                
    Queremos recopilar información de los profesionales que participan.  
    Tu colaboración permitirá validar el prototipo para realizar una investigación.  

    ---

    ⚠️ **Atención:** al finalizar el Cuestionario de validación en la última pestaña, les pedimos por favor que luego de llenar todos los campos den click en **Enviar feedback**, luego den click en **Copiar feedback** y finalmente den click en **Enviar feedback por WhatsApp**.
    """)



# ----------------------------
# Pestaña 2: Registro de datos del profesional
# ----------------------------
with tabs[1]:
    st.header("Registro de datos del profesional")
    
    nombre_prof = st.text_input("Nombre completo", key="prof_nombre")
    profesion_prof = st.text_input("Profesión", key="prof_profesion")
    cedula_prof = st.text_input("Cédula", key="prof_cedula")

    if st.button("Registrar datos profesionales", key="btn_registrar_prof"):
        if nombre_prof and profesion_prof and cedula_prof:
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

    st.markdown("En la pestaña siguiente comienza el prototipo de formulario web para cada paciente.", unsafe_allow_html=True)

# ----------------------------
# Pestaña 3: Datos del paciente
# ----------------------------
with tabs[2]:
    st.header("Datos del paciente")
    
    columnas = ["Nombre", "Escolaridad", "Fecha", "Hora"]
    
    if os.path.exists(PACIENTES_FILE):
        df_pacientes = pd.read_csv(PACIENTES_FILE)
        for col in columnas:
            if col not in df_pacientes.columns:
                df_pacientes[col] = ""
        df_pacientes = df_pacientes[columnas]
    else:
        df_pacientes = pd.DataFrame(columns=columnas)

    st.subheader("Pacientes registrados (editable)")
    edited_df = st.data_editor(df_pacientes, num_rows="dynamic", use_container_width=True, key="pacientes_editor")

    if st.button("Guardar cambios en la tabla", key="guardar_pacientes"):
        edited_df.to_csv(PACIENTES_FILE, index=False)
        st.success("Cambios guardados correctamente.")

# ----------------------------
# Pestaña 4: Antecedentes
# ----------------------------
with tabs[3]:
    st.header("Antecedentes")
    with st.form("form_antecedentes"):
        datos_relevantes = st.text_area("Ingrese los datos relevantes", key="antec_datos")
        derivado_por = st.text_input("Derivado por:", key="antec_derivado")
        motivo_consulta = st.text_area("Motivo de consulta", key="antec_motivo")
        submitted_antec = st.form_submit_button("Guardar antecedentes")
        if submitted_antec:
            st.success("Antecedentes guardados correctamente!")

# ----------------------------
# Pestaña 5: Entrevista inicial
# ----------------------------
with tabs[4]:
    st.header("Entrevista inicial")
    with st.form("form_entrevista"):
        st.subheader("Datos Perinatales")
        peso = st.text_input("Peso", key="peri_peso")
        talla = st.text_input("Talla", key="peri_talla")
        apgar = st.text_input("APGAR", key="peri_apgar")

        st.subheader("Primeros contactos con la madre")
        amamantamiento = st.text_area("Amamantamiento cómo y hasta cuándo", key="amamantamiento")

        st.subheader("Desarrollo neuropsíquico")
        control_cefalico = st.text_input("Control cefálico (edad)", key="neuro_cefalico")
        gateo = st.text_input("Gateo (edad y cómo fue aprendizaje)", key="neuro_gateo")
        marcha = st.text_input("Marcha independiente (edad)", key="neuro_marcha")
        esfinteres = st.text_input("Control de esfínteres (edad y aprendizaje)", key="neuro_esfinteres")
        lenguaje = st.text_area("Lenguaje (primeras palabras / dificultades)", key="neuro_lenguaje")
        praxias = st.text_area("Adquisición de praxias", key="neuro_praxias")

        st.subheader("Ritmos")
        sueno = st.text_area("Sueño: cómo se duerme / cómo duerme", key="ritmo_sueno")
        colecho = st.text_input("Colecho (sí/no)", key="ritmo_colecho")
        cohabitacion = st.text_input("Cohabitación (sí/no)", key="ritmo_cohabitacion")
        alimentacion = st.text_area("Alimentación: transición líquida a semi-sólida, hábitos", key="ritmo_alimentacion")

        st.subheader("Escolaridad")
        primera_escolarizacion = st.text_area("Primera escolarización / adaptación / instituciones / año en curso", key="escolaridad_inicial")
        lecto_escritura = st.text_area("Aprendizaje de la lecto-escritura / gusto por la escuela / opinión de padres", key="escolaridad_lecto")

        st.subheader("Social y Juegos")
        amigos = st.text_area("Amigos, cómo se relaciona y juegos", key="social_amigos")
        actividades = st.text_area("Otras actividades especiales", key="social_actividades")
        tiempo_pantalla = st.text_input("Horas dedicadas a TV/PC", key="social_tiempo")

        st.subheader("Límites")
        acepta_limites = st.text_area("Acepta los límites y reacción frente al 'no'", key="limites_acepta")
        estrategias_padres = st.text_area("Estrategias de los padres para aprendizaje de normas", key="limites_estrategias")

        antecedentes_familiares = st.text_area("Antecedentes familiares relevantes", key="antec_familiares")

        submitted_entrevista = st.form_submit_button("Guardar entrevista")
        if submitted_entrevista:
            campos_obligatorios = [peso, talla, apgar, amamantamiento, control_cefalico, gateo, marcha, esfinteres, lenguaje, praxias, sueno, colecho, cohabitacion, alimentacion, primera_escolarizacion, lecto_escritura, amigos, actividades, tiempo_pantalla, acepta_limites, estrategias_padres, antecedentes_familiares]
            campos_vacios = any([str(c).strip() == '' for c in campos_obligatorios])
            if campos_vacios:
                st.error("Por favor completá todos los campos obligatorios antes de guardar la entrevista inicial.")
            else:
                st.success("Entrevista inicial guardada correctamente!")

# ----------------------------
# Pestaña 6: Exploración
# ----------------------------
with tabs[5]:
    st.header("Exploración")
    with st.form("form_exploracion"):
        imagen = st.file_uploader("Ingresar imagen", type=["jpg","png","jpeg"], key="exploracion_img")
        submitted_exploracion = st.form_submit_button("Guardar exploración")
        if submitted_exploracion:
            st.success("Exploración guardada correctamente!")

# ----------------------------
# Pestaña 7: Tests psicomotrices
# ----------------------------
with tabs[6]:
    st.header("Tests psicomotrices")
    tests_disponibles = [
        "DFH Koppitz",
        "Reversal Test",
        "Test de Figura Completa",
        "Test de Escritura de Ajuriaguerra",
        "Test de Bender",
        "Esquema Corporal Vitor da Fonseca",
        "Batería Piaget-Head",
        "Test de Dibujo Libre",
        "Test de Frostig",
        "Test de Pascual"
    ]
    with st.form("form_tests"):
        seleccionados = st.multiselect("Seleccione los tests realizados", tests_disponibles, key="tests_sel")
        resultados = st.text_area("Detalle los resultados de los tests", key="tests_res")
        submitted_tests = st.form_submit_button("Guardar tests")
        if submitted_tests:
            st.success("Tests guardados correctamente!")

# ----------------------------
# Pestaña 8: Seguimiento del proceso
# ----------------------------
with tabs[7]:
    st.header("Seguimiento del proceso")
    with st.form("form_seguimiento"):
        notas_clinicas = st.text_area("Notas de relevancia clínica", key="seguimiento_notas")
        ideas_vinculares = st.text_area("Ideas cualitativas sobre el proceso vincular", key="seguimiento_ideas")
        motor = st.text_area("Motor", key="seguimiento_motor")
        afectivo = st.text_area("Afectivo", key="seguimiento_afectivo")
        relacional = st.text_area("Relacional", key="seguimiento_relacional")
        submitted_seguimiento = st.form_submit_button("Guardar seguimiento")
        if submitted_seguimiento:
            st.success("Seguimiento guardado correctamente!")

# ----------------------------
# Pestaña 9: Guardar evaluación completa
# ----------------------------
with tabs[8]:
    st.header("Guardar Evaluación Completa")
    with st.form("form_guardar"):
        comentario_final = st.text_area("Comentarios finales antes de guardar evaluación", key="guardar_comentario")
        submitted_final = st.form_submit_button("Guardar evaluación")
        if submitted_final:
            st.success("Evaluación completa guardada!")

# ----------------------------
# Pestaña 10: Lista de pacientes registrados
# ----------------------------
with tabs[9]:
    st.header("📋 Lista de pacientes registrados")
    if os.path.exists(PACIENTES_FILE):
        df_pacientes = pd.read_csv(PACIENTES_FILE)
        columnas = ["Nombre", "Escolaridad", "Fecha", "Hora"]
        for col in columnas:
            if col not in df_pacientes.columns:
                df_pacientes[col] = ""
        df_pacientes = df_pacientes[columnas]
        st.dataframe(df_pacientes)
    else:
        st.info("No hay pacientes registrados aún.")

# ----------------------------
# Pestaña 11: Cuestionario de validación
# ----------------------------
with tabs[10]:
    st.header("✅ Cuestionario de validación de la app")
    
    # Primero pedir el nombre del profesional (obligatorio)
    nombre_profesional = st.text_input("Nombre y apellido del profesional*", key="feedback_nombre")
    
    with st.form("form_feedback"):
        utilidad_map = {"Mucho": 5, "Algo": 3, "Nada": 1}
        eficiencia_map = {"Sí": 5, "Parcialmente": 3, "No": 1}
        satisfaccion_map = {"Sí": 5, "Parcialmente": 3, "No": 1}
        diseño_map = {"Muy bueno": 5, "Bueno": 4, "Regular": 3, "Malo": 2, "Muy malo": 1}

        utilidad_resp = st.radio(
            "¿Este formulario digital le facilitaría su trabajo comparado con el método actual?",
            ["Mucho", "Algo", "Nada"], key="feedback_utilidad"
        )
        eficiencia_resp = st.radio(
            "¿Cree que este formulario ayuda a que sus procesos sean más eficientes?",
            ["Sí", "Parcialmente", "No"], key="feedback_eficiencia"
        )
        intencion_uso = st.slider(
            "En una escala del 0 al 10, ¿qué probabilidad tiene de usar esta app regularmente?",
            0, 10, 7, key="feedback_intencion"
        )
        satisfaccion_claridad = st.radio(
            "¿Considera que el formulario es claro y fácil de completar?",
            ["Sí", "Parcialmente", "No"], key="feedback_satisfaccion_claridad"
        )
        satisfaccion_diseño = st.radio(
            "Cómo evalúa el diseño visual de la app?",
            ["Muy bueno", "Bueno", "Regular", "Malo", "Muy malo"], key="feedback_satisfaccion_diseño"
        )
        modificar_secciones = st.text_area(
            "¿Qué agregarían o modificarían en las secciones existentes?",
            key="feedback_modificar"
        )
        comentarios = st.text_area(
            "Comentarios o sugerencias adicionales (respuesta libre)",
            key="feedback_comentarios"
        )
        
        submitted_feedback = st.form_submit_button("Enviar feedback")
        
    # Manejo de la respuesta del formulario
    if submitted_feedback:
        # Validación de campos obligatorios
        if not nombre_profesional.strip():
            st.error("Por favor ingrese su nombre y apellido (campo obligatorio).")
        else:
            # Validar otros campos obligatorios
            campos_obligatorios = [utilidad_resp, eficiencia_resp, intencion_uso, satisfaccion_claridad, satisfaccion_diseño, modificar_secciones, comentarios]
            campos_vacios = any([str(c).strip() == '' for c in campos_obligatorios])
            
            if campos_vacios:
                st.error("Por favor completá todas las respuestas obligatorias antes de enviar.")
            else:
                utilidad_val = utilidad_map[utilidad_resp]
                eficiencia_val = eficiencia_map[eficiencia_resp]
                satisfaccion_claridad_val = satisfaccion_map[satisfaccion_claridad]
                satisfaccion_diseño_val = diseño_map[satisfaccion_diseño]

                nueva_fila = pd.DataFrame({
                    "nombre_profesional": [nombre_profesional],
                    "utilidad": [utilidad_val],
                    "utilidad_opcion": [utilidad_resp],
                    "eficiencia": [eficiencia_val],
                    "eficiencia_opcion": [eficiencia_resp],
                    "intencion_uso": [intencion_uso],
                    "satisfaccion_claridad": [satisfaccion_claridad_val],
                    "satisfaccion_claridad_opcion": [satisfaccion_claridad],
                    "satisfaccion_diseño": [satisfaccion_diseño_val],
                    "satisfaccion_diseño_opcion": [satisfaccion_diseño],
                    "modificar_secciones": [modificar_secciones],
                    "comentarios": [comentarios],
                    "fecha_envio": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                })

                if os.path.exists(FEEDBACK_FILE):
                    df_feedback = pd.read_csv(FEEDBACK_FILE)
                    df_feedback = pd.concat([df_feedback, nueva_fila], ignore_index=True)
                else:
                    df_feedback = nueva_fila
                df_feedback.to_csv(FEEDBACK_FILE, index=False)
                st.success("¡Gracias! Tu feedback fue registrado correctamente!")

                resumen_compacto = (
                    f"Feedback App\n"
                    f"Nombre del profesional: {nombre_profesional}\n"
                    f"Utilidad: {utilidad_resp} ({utilidad_val}/5)\n"
                    f"Eficiencia: {eficiencia_resp} ({eficiencia_val}/5)\n"
                    f"Intención de uso: {intencion_uso}/10\n"
                    f"Satisfacción claridad: {satisfaccion_claridad} ({satisfaccion_claridad_val}/5)\n"
                    f"Satisfacción diseño: {satisfaccion_diseño} ({satisfaccion_diseño_val}/5)\n"
                    f"Modificar secciones: {modificar_secciones}\n"
                    f"Comentarios: {comentarios}"
                )
                st.markdown('<h4>Resumen generado:</h4>', unsafe_allow_html=True)
                st.code(resumen_compacto, language=None)

                copy_code = f'''
<button id="copyBtn" style="background-color:#25D366;color:white;padding:1em 2em;font-size:1.2em;border:none;border-radius:8px;font-weight:bold;cursor:pointer;">📋 Copiar feedback</button>
<script>
document.getElementById('copyBtn').onclick = function(){{
    navigator.clipboard.writeText(`{resumen_compacto}`);
    alert('¡Resumen copiado! Ahora pégalo en WhatsApp.');
}}
</script>
'''
                components.html(copy_code, height=80)

                mensaje_codificado = urllib.parse.quote_plus(resumen_compacto)
                numero = "59898776605"
                js_code = f'''
<button id="wappBtn" style="background-color:#25D366;color:white;padding:1em 2em;font-size:1.2em;border:none;border-radius:8px;font-weight:bold;cursor:pointer;margin-top:1em;">💬 Enviar feedback por WhatsApp</button>
<script>
document.getElementById('wappBtn').onclick = function(){{
    var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    var url = '';
    if (isMobile){{
        url = 'https://wa.me/?text={mensaje_codificado}';
    }} else {{
        url = 'https://web.whatsapp.com/send?phone={numero}&text={mensaje_codificado}';
    }}
    window.open(url, '_blank');
}}
</script>
'''
                components.html(js_code, height=120)
