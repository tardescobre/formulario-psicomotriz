# Streamlit + Python base
FROM python:3.11-slim

WORKDIR /app

# System deps (optional minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Streamlit config
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_BROWSER_SERVER_ADDRESS=0.0.0.0

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
