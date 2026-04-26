# Marrim Python si bazë
FROM python:3.11-slim

# Krijojmë folderin e punës
WORKDIR /app

# Kopjojmë requirements fillimisht (për cache)
COPY requirements.txt .

# Instalojmë dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Kopjojmë kodin
COPY . .

# API dëgjon në portin 8000
EXPOSE 8000

# Startojmë API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]