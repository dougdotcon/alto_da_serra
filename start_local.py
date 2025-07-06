import subprocess
import sys
import os
import time
import webbrowser

# Caminhos
BACKEND_DIR = os.path.join(os.getcwd(), 'backend')
FRONTEND_DIR = os.path.join(os.getcwd(), 'frontend')

# Comandos
BACKEND_CMD = [sys.executable, '-m', 'uvicorn', 'api:app', '--reload', '--host', '127.0.0.1', '--port', '8000']
FRONTEND_CMD = [sys.executable, 'manage.py', 'runserver', '127.0.0.1:8080']

def main():
    print('🚀 Iniciando Alto da Serra - Sistema de Restaurante')
    print('=' * 50)

    # Iniciar backend
    print('📡 Iniciando backend FastAPI...')
    backend_proc = subprocess.Popen(BACKEND_CMD, cwd=BACKEND_DIR)
    print('✅ Backend iniciado em http://127.0.0.1:8000')
    time.sleep(3)  # Delay para garantir que o backend suba antes do frontend

    # Iniciar frontend Django
    print('🌐 Iniciando frontend Django...')
    frontend_proc = subprocess.Popen(FRONTEND_CMD, cwd=FRONTEND_DIR)
    print('✅ Frontend Django iniciado em http://127.0.0.1:8080')

    # Aguardar um pouco e abrir o navegador
    time.sleep(3)
    print('🌍 Abrindo navegador...')
    webbrowser.open('http://127.0.0.1:8080')

    print('\n' + '=' * 50)
    print('🎉 Sistema iniciado com sucesso!')
    print('📋 Acesse: http://127.0.0.1:8080')
    print('🔑 Login: adm / 123 ou a / a')
    print('⚠️  Pressione Ctrl+C para encerrar')
    print('=' * 50)

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print('\n🛑 Encerrando sistema...')
        backend_proc.terminate()
        frontend_proc.terminate()
        print('✅ Sistema encerrado com sucesso!')

if __name__ == '__main__':
    main() 