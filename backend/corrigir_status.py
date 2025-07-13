import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("restaurante.db")
cursor = conn.cursor()

# Verificar status atuais
print("Status atuais:")
cursor.execute("SELECT id, status FROM status_mesas ORDER BY id")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Status: {row[1]}")

print("\n--- Corrigindo status 'Aberta' para 'Aberto' ---")

# Corrigir o status "Aberta" para "Aberto"
cursor.execute("UPDATE status_mesas SET status = ? WHERE status = ?", ("Aberto", "Aberta"))
print(f"Registros atualizados: {cursor.rowcount}")

# Verificar se precisa adicionar o status "Aberto" caso não exista
cursor.execute("SELECT COUNT(*) FROM status_mesas WHERE status = 'Aberto'")
count_aberto = cursor.fetchone()[0]

if count_aberto == 0:
    print("Status 'Aberto' não encontrado, adicionando...")
    cursor.execute("INSERT INTO status_mesas (status) VALUES (?)", ("Aberto",))
    print("Status 'Aberto' adicionado")

# Verificar status finais
print("\nStatus após correção:")
cursor.execute("SELECT id, status FROM status_mesas ORDER BY id")
for row in cursor.fetchall():
    print(f"ID: {row[0]}, Status: {row[1]}")

# Verificar quantas mesas têm status inválido e corrigir se necessário
print("\n--- Verificando mesas com status inválido ---")
cursor.execute("""
    SELECT m.id, m.status_id, sm.status 
    FROM mesas m 
    LEFT JOIN status_mesas sm ON m.status_id = sm.id 
    WHERE sm.status IS NULL
""")
mesas_invalidas = cursor.fetchall()

if mesas_invalidas:
    print(f"Encontradas {len(mesas_invalidas)} mesas com status inválido")
    # Definir status padrão como "Livre" (ID 1)
    cursor.execute("SELECT id FROM status_mesas WHERE status = 'Livre'")
    livre_id = cursor.fetchone()[0]
    
    for mesa in mesas_invalidas:
        cursor.execute("UPDATE mesas SET status_id = ? WHERE id = ?", (livre_id, mesa[0]))
        print(f"Mesa {mesa[0]} atualizada para status 'Livre'")
else:
    print("Todas as mesas têm status válidos")

# Salvar alterações
conn.commit()
conn.close()

print("\nCorreção concluída!")
