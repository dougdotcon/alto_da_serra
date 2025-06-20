import sqlite3

conn = sqlite3.connect("restaurante.db")
cursor = conn.cursor()

# Inserir configuração do restaurante
cursor.execute("INSERT INTO configuracoes (nome_restaurante, quantidade_mesas) VALUES (?, ?)",
               ("Alto da Serra", 50))

# Inserir tipos de usuários
tipos_usuarios = ["garcom", "caixa", "adm"]
cursor.executemany("INSERT INTO tipos_usuarios (nome) VALUES (?)", [(t,) for t in tipos_usuarios])

# Inserir status das mesas
status_mesas = ["Aberto", "Fechada", "Reservada"]
cursor.executemany("INSERT INTO status_mesas (status) VALUES (?)", [(s,) for s in status_mesas])

# Inserir tipos de quantidade
tipos_quantidade = ["unitario", "kg"]
cursor.executemany("INSERT INTO tipos_quantidade (nome) VALUES (?)", [(t,) for t in tipos_quantidade])

# Inserir mesas M1 até M50 com status inicial 'Aberto'
cursor.execute("SELECT id FROM status_mesas WHERE status = 'Aberto'")
status_aberto_id = cursor.fetchone()[0]

for i in range(1, 51):
    mesa_id = f"M{i}"
    cursor.execute("""
        INSERT INTO mesas (id, status_id, cliente, data_abertura, valor_total, em_uso_por)
        VALUES (?, ?, NULL, NULL, 0.0,"livre")
    """, (mesa_id, status_aberto_id))

conn.commit()
conn.close()

print("Dados iniciais inseridos com sucesso!")
