import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("restaurante.db")
cursor = conn.cursor()

print("🔄 Atualizando valores totais das mesas...")

# Atualizar valor_total de todas as mesas baseado no consumo atual
cursor.execute("""
    UPDATE mesas 
    SET valor_total = (
        SELECT COALESCE(SUM(c.total), 0) 
        FROM consumo c 
        WHERE c.mesa_id = mesas.id
    )
""")

print(f"✅ {cursor.rowcount} mesas atualizadas")

# Verificar os valores atualizados
print("\n📊 Valores totais das mesas:")
cursor.execute("""
    SELECT m.id, m.cliente, m.valor_total, 
           COALESCE(SUM(c.total), 0) as total_consumo,
           COUNT(c.id) as itens_consumo
    FROM mesas m
    LEFT JOIN consumo c ON m.id = c.mesa_id
    GROUP BY m.id, m.cliente, m.valor_total
    ORDER BY m.id
""")

for row in cursor.fetchall():
    mesa_id, cliente, valor_total, total_consumo, itens = row
    status_icon = "✅" if valor_total == total_consumo else "❌"
    print(f"{status_icon} Mesa {mesa_id}: Valor Total: R${valor_total:.2f} | Consumo: R${total_consumo:.2f} | Itens: {itens}")
    if cliente:
        print(f"    Cliente: {cliente}")

# Salvar alterações
conn.commit()
conn.close()

print("\n🎉 Atualização concluída!")
