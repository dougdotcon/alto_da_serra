import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("restaurante.db")
cursor = conn.cursor()

print("=== DEBUG: Verificando consumo e produtos ===")

# Verificar produtos existentes
print("\n1. Produtos cadastrados:")
cursor.execute("SELECT id, nome, preco_venda FROM produtos ORDER BY id")
produtos = cursor.fetchall()
for produto in produtos:
    print(f"   ID: {produto[0]}, Nome: {produto[1]}, Preço: R$ {produto[2]:.2f}")

if not produtos:
    print("   ⚠️ NENHUM PRODUTO ENCONTRADO!")

# Verificar consumo da mesa M1
print("\n2. Consumo da mesa M1:")
cursor.execute("""
    SELECT c.id, c.produto_id, p.nome, c.quantidade, c.total, c.mesa_id
    FROM consumo c
    LEFT JOIN produtos p ON c.produto_id = p.id
    WHERE c.mesa_id = 'M1'
""")
consumo_m1 = cursor.fetchall()

if consumo_m1:
    for item in consumo_m1:
        print(f"   Consumo ID: {item[0]}, Produto ID: {item[1]}, Nome: {item[2]}, Qtd: {item[3]}, Total: R$ {item[4]:.2f}, Mesa: {item[5]}")
else:
    print("   ⚠️ NENHUM CONSUMO ENCONTRADO PARA A MESA M1!")

# Verificar todas as mesas com consumo
print("\n3. Todas as mesas com consumo:")
cursor.execute("""
    SELECT DISTINCT mesa_id, COUNT(*) as itens
    FROM consumo
    GROUP BY mesa_id
    ORDER BY mesa_id
""")
mesas_com_consumo = cursor.fetchall()

if mesas_com_consumo:
    for mesa in mesas_com_consumo:
        print(f"   Mesa: {mesa[0]}, Itens: {mesa[1]}")
else:
    print("   ⚠️ NENHUMA MESA TEM CONSUMO!")

# Verificar status da mesa M1
print("\n4. Status da mesa M1:")
cursor.execute("""
    SELECT m.id, m.cliente, s.status, m.valor_total
    FROM mesas m
    LEFT JOIN status_mesas s ON m.status_id = s.id
    WHERE m.id = 'M1'
""")
mesa_m1 = cursor.fetchone()

if mesa_m1:
    print(f"   Mesa: {mesa_m1[0]}, Cliente: {mesa_m1[1]}, Status: {mesa_m1[2]}, Total: R$ {mesa_m1[3]:.2f}")
else:
    print("   ⚠️ MESA M1 NÃO ENCONTRADA!")

# Verificar se existe algum log de inserção recente
print("\n5. Últimos registros na tabela consumo:")
cursor.execute("""
    SELECT c.id, c.produto_id, p.nome, c.quantidade, c.total, c.mesa_id
    FROM consumo c
    LEFT JOIN produtos p ON c.produto_id = p.id
    ORDER BY c.id DESC
    LIMIT 10
""")
ultimos_consumos = cursor.fetchall()

if ultimos_consumos:
    for item in ultimos_consumos:
        print(f"   ID: {item[0]}, Produto: {item[1]} ({item[2]}), Qtd: {item[3]}, Total: R$ {item[4]:.2f}, Mesa: {item[5]}")
else:
    print("   ⚠️ NENHUM REGISTRO DE CONSUMO ENCONTRADO!")

conn.close()
print("\n=== FIM DO DEBUG ===")
