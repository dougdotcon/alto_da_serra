import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("restaurante.db")
cursor = conn.cursor()

# Verificar se o status "Livre" já existe
cursor.execute("SELECT COUNT(*) FROM status_mesas WHERE status = 'Livre'")
count = cursor.fetchone()[0]

if count == 0:
    print("Adicionando status 'Livre'...")
    cursor.execute("INSERT INTO status_mesas (id, status) VALUES (4, 'Livre')")
    print("Status 'Livre' adicionado com ID 4")
else:
    print("Status 'Livre' já existe")

# Reorganizar para que Livre seja ID 1, Aberto seja ID 2, etc.
print("Reorganizando ordem dos status...")

# Criar tabela temporária com a ordem correta
cursor.execute("DROP TABLE IF EXISTS status_temp")
cursor.execute("""
    CREATE TABLE status_temp (
        id INTEGER PRIMARY KEY,
        status TEXT UNIQUE NOT NULL
    )
""")

# Inserir na ordem correta
cursor.execute("INSERT INTO status_temp (id, status) VALUES (1, 'Livre')")
cursor.execute("INSERT INTO status_temp (id, status) VALUES (2, 'Aberto')")
cursor.execute("INSERT INTO status_temp (id, status) VALUES (3, 'Fechada')")
cursor.execute("INSERT INTO status_temp (id, status) VALUES (4, 'Reservada')")

# Atualizar as referências nas mesas primeiro
cursor.execute("""
    UPDATE mesas 
    SET status_id = CASE 
        WHEN status_id = (SELECT id FROM status_mesas WHERE status = 'Livre') THEN 1
        WHEN status_id = (SELECT id FROM status_mesas WHERE status = 'Aberto') THEN 2  
        WHEN status_id = (SELECT id FROM status_mesas WHERE status = 'Fechada') THEN 3
        WHEN status_id = (SELECT id FROM status_mesas WHERE status = 'Reservada') THEN 4
        ELSE 1
    END
""")

# Substituir a tabela original
cursor.execute("DROP TABLE status_mesas")
cursor.execute("ALTER TABLE status_temp RENAME TO status_mesas")

conn.commit()

# Verificar resultado final
cursor.execute("SELECT id, status FROM status_mesas ORDER BY id")
print("\nStatus finais:")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Status: {row[1]}")

conn.close()
print("\nReorganização concluída!")
