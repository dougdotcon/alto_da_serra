import sqlite3
import os

def criar_usuario_admin():
    DB_PATH = os.path.join(os.path.dirname(__file__), "restaurante.db")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Verificar se já existe um usuário admin
    cursor.execute("SELECT id FROM usuarios WHERE user = 'adm'")
    if cursor.fetchone():
        print("Usuário administrador já existe!")
        return
    
    # Pegar o ID do tipo_usuario 'adm'
    cursor.execute("SELECT id FROM tipos_usuarios WHERE nome = 'adm'")
    tipo_admin = cursor.fetchone()
    
    if not tipo_admin:
        print("Tipo de usuário 'adm' não encontrado. Verifique se inserir_dados.py foi executado.")
        return
        
    # Inserir usuário administrador
    cursor.execute("""
        INSERT INTO usuarios (user, senha, nome, tipo_usuario_id)
        VALUES (?, ?, ?, ?)
    """, ('adm', '123', 'Administrador', tipo_admin[0]))
    
    conn.commit()
    conn.close()
    print("Usuário administrador criado com sucesso!")

if __name__ == "__main__":
    criar_usuario_admin()