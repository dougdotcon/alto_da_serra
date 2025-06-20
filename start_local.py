import subprocess
import sys
import os
import time

# Caminhos
BACKEND_DIR = os.path.join(os.getcwd(), 'backend')
FRONTEND_DIR = os.path.join(os.getcwd(), 'frontend')

# Comandos
BACKEND_CMD = [sys.executable, '-m', 'uvicorn', 'api:app', '--reload', '--host', '127.0.0.1', '--port', '8000']
FRONTEND_CMD = [sys.executable, 'login.py']

def main():
    # Iniciar backend
    backend_proc = subprocess.Popen(BACKEND_CMD, cwd=BACKEND_DIR)
    print('Backend iniciado em http://127.0.0.1:8000')
    time.sleep(2)  # Pequeno delay para garantir que o backend suba antes do frontend

    # Iniciar frontend
    frontend_proc = subprocess.Popen(FRONTEND_CMD, cwd=FRONTEND_DIR)
    print('Frontend iniciado.')

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print('Encerrando...')
        backend_proc.terminate()
        frontend_proc.terminate()

if __name__ == '__main__':
    main() 