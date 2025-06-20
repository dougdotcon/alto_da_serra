#!/bin/bash

# Inicia o backend FastAPI
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Aguarda alguns segundos para garantir que a API esteja no ar
sleep 2

# Inicia o frontend Flet
python3 frontend/login.py
