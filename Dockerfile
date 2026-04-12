FROM python:3.11-slim
WORKDIR /app

# 1. Install system tools
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# 2. Install dependencies
# Added 'requests' which is needed for the wait-loop in inference.py
RUN pip install --no-cache-dir \
    fastapi==0.110.0 \
    uvicorn==0.27.1 \
    python-dotenv==1.0.1 \
    pyautogen==0.2.27 \
    requests \
    openenv-core>=0.2.0

# 3. Copy files
COPY . .

# 4. Set environment
ENV PYTHONPATH=/app
EXPOSE 7860

# 5. Start
# Using 7860 as requested by the hackathon validator logs
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
