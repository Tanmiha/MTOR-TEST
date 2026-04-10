FROM python:3.11-slim
WORKDIR /app

# 1. Install system tools
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

# 2. FORCE INSTALL (THE "NUKE" STEP)
# We add a dummy echo here to break the cache and force a re-download.
# 'pyautogen' is the pip package name. 'autogen' is the import name.
RUN echo "Forcing fresh install - v2" && \
    pip install --no-cache-dir \
    fastapi==0.110.0 \
    uvicorn==0.27.1 \
    python-dotenv==1.0.1 \
    pyautogen==0.2.27 \
    openenv-core>=0.2.0

# 3. Copy files
COPY . .

# 4. Set environment
ENV PYTHONPATH=/app
EXPOSE 8000

# 5. Start
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
