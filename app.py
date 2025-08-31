import streamlit as st
import pandas as pd
import os

# Definir DATA_FOLDER si no existe
if 'DATA_FOLDER' not in globals():
    DATA_FOLDER = '.'

# Definir tabs si no existe
if 'tabs' not in globals():
    tabs = st.tabs([
        "Datos del paciente",
        "Antecedentes",
        "Tests psicomotrices",
        "Seguimiento del proceso",
        "Guardar evaluación",
        "Cuestionario de validación",
        "Lista de pacientes"
    ])
with tabs[0]:
    st.header("Datos del paciente")
    with st.form("form_paciente"):
        nombre = st.text_input("Nombre completo")
        documento = st.text_input("Documento")
        edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
        sexo = st.selectbox("Sexo", ["", "Masculino", "Femenino", "Otro"])
        derivado = st.radio("¿Fue derivado?", ["Sí", "No"])
        fuente_derivacion = st.text_input("Fuente de derivación (ej: escuela, pediatra)")
        motivo_consulta = st.text_area("Motivo de consulta")
        submitted_paciente = st.form_submit_button("Guardar paciente")
        if submitted_paciente:
            import datetime
            import csv
            datos = {
                "timestamp": datetime.datetime.now().isoformat(),
                "nombre": nombre,
                "documento": documento,
                "edad": edad,
                "sexo": sexo,
                "derivado": derivado,
                "fuente_derivacion": fuente_derivacion,
                "motivo_consulta": motivo_consulta
            }
            archivo = "registros.csv"
            existe = os.path.exists(archivo)
            with open(archivo, "a", newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=datos.keys())
                if not existe:
                    writer.writeheader()
                writer.writerow(datos)
            st.success("Paciente guardado correctamente.")





with tabs[1]:
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

with tabs[2]:
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

with tabs[3]:
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

with tabs[4]:
    st.header("Guardar evaluación completa")
    with st.form("form_guardar"):
        comentario_final = st.text_area("Comentarios finales antes de guardar evaluación")
        submitted_final = st.form_submit_button("Guardar evaluación")

with tabs[5]:
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
            # Advertencia para usuarios de WhatsApp Desktop
            st.warning("""
**IMPORTANTE:** Si tienes WhatsApp Desktop instalado, el mensaje NO se prellenará automáticamente. 

Para que el texto se complete solo, usa WhatsApp Web (web.whatsapp.com) o la app móvil. 

Si no funciona, puedes copiar el resumen manualmente y pegarlo en tu chat de WhatsApp.
""")

            # Resumen real del feedback
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

            # Mostrar el resumen y botón para copiar
            import streamlit.components.v1 as components
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

            import urllib.parse
            mensaje_codificado = urllib.parse.quote_plus(resumen_compacto)
            numero = "59898776605"
            link_whatsapp = f"https://wa.me/{numero}?text={mensaje_codificado}"
            st.markdown(
                f"""
                <a href="{link_whatsapp}" target="_blank" style="
                    display: inline-block;
                    padding: 1em 2em;
                    font-size: 1.2em;
                    color: white;
                    background-color: #25D366;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: bold;
                    margin-top: 1em;
                ">💬 Enviar feedback por WhatsApp</a>
                """,
                unsafe_allow_html=True
            )

with tabs[6]:
    st.header("📋 Lista de pacientes registrados")
    try:
        df_pacientes = pd.read_csv("registros.csv")
        st.dataframe(df_pacientes)
    except Exception as e:
        st.info("No hay registros de pacientes aún o el archivo no existe.")






                            
