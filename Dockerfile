FROM python:3.11-slim

WORKDIR /app

# Copia tudo para o container
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY config.json ./

# Instala dependências
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expõe porta para Cloud Run
EXPOSE 8080

# Comando que roda API e Flet ao mesmo tempo
CMD ["bash", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8080 & python3 frontend/login.py"]


COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]
