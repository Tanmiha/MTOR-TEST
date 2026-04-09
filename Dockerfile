FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ADD THESE
RUN pip install fastapi uvicorn streamlit

COPY . .

EXPOSE 7860

CMD bash -c "uvicorn api:app --host 0.0.0.0 --port 7860 & streamlit run app.py --server.port=8501 --server.address=0.0.0.0"