# Formulario Psicomotriz

Aplicación Streamlit para registro de profesionales y feedback.

## Estructura de datos
- `datos_guardados/feedback_app.csv` (canónico)
- `datos_guardados/profesionales.csv`
- `datos_guardados/pacientes.csv`

## Desarrollo local
```powershell
cd C:\Users\HP\AppData\Local\Programs\Python\Python313\evaluaciones
streamlit run app.py
```

## Despliegue

### Opción A: Streamlit Community Cloud
1. Pushea la rama `main` a GitHub (listo).
2. Ve a https://share.streamlit.io , "Deploy an app" y apunta al repo `tardescobre/formulario-psicomotriz` (o el que corresponda), archivo `app.py`, rama `main`.
3. Variables/Secrets: no requeridas.
4. Deploy.

### Opción B: Render (Free Web Service)
1. Conecta el repo y elige "Web Service".
2. Runtime: Docker.
3. Puerto: 8501.
4. `Dockerfile` ya incluido.

### Opción C: Docker manual
```powershell
# build
docker build -t formulario-psico:latest .
# run
docker run -p 8501:8501 -v %cd%\datos_guardados:/app/datos_guardados formulario-psico:latest
```

> Nota: El volumen mantiene los CSV en el host.

## Seguridad
- El guardado de feedback está blindado (escritura atómica + verificación).
- CSVs en UTF-8-BOM y quoting seguro.
