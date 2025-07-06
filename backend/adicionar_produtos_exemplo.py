import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "restaurante.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Produtos de exemplo para um restaurante
produtos_exemplo = [
    # Bebidas
    ("7891000100103", "Coca-Cola 350ml", "Lote001", "Coca-Cola", 1, "2025-12-31", 2.50, 5.00),
    ("7891000100110", "Guaraná Antarctica 350ml", "Lote002", "Antarctica", 1, "2025-12-31", 2.30, 4.50),
    ("7891000100127", "Água Mineral 500ml", "Lote003", "Crystal", 1, "2026-06-30", 1.00, 3.00),
    ("7891000100134", "Suco de Laranja 300ml", "Lote004", "Maguary", 1, "2025-08-15", 3.00, 6.00),
    ("7891000100141", "Cerveja Skol 350ml", "Lote005", "Skol", 1, "2025-10-20", 2.80, 6.50),
    
    # Pratos principais
    ("7891000200101", "Hambúrguer Artesanal", "Lote101", "Casa", 1, "", 8.00, 18.00),
    ("7891000200118", "Pizza Margherita", "Lote102", "Casa", 1, "", 12.00, 25.00),
    ("7891000200125", "Lasanha Bolonhesa", "Lote103", "Casa", 1, "", 10.00, 22.00),
    ("7891000200132", "Filé de Frango Grelhado", "Lote104", "Casa", 1, "", 9.00, 20.00),
    ("7891000200149", "Salada Caesar", "Lote105", "Casa", 1, "", 6.00, 15.00),
    
    # Sobremesas
    ("7891000300108", "Pudim de Leite", "Lote201", "Casa", 1, "", 3.00, 8.00),
    ("7891000300115", "Torta de Chocolate", "Lote202", "Casa", 1, "", 4.00, 12.00),
    ("7891000300122", "Sorvete 2 Bolas", "Lote203", "Kibon", 1, "2025-09-30", 2.50, 7.00),
    ("7891000300139", "Mousse de Maracujá", "Lote204", "Casa", 1, "", 3.50, 9.00),
    
    # Petiscos
    ("7891000400105", "Batata Frita Porção", "Lote301", "Casa", 2, "", 2.00, 8.00),
    ("7891000400112", "Pastéis 6 unidades", "Lote302", "Casa", 1, "", 4.00, 12.00),
    ("7891000400129", "Porção de Mandioca", "Lote303", "Casa", 2, "", 1.50, 6.00),
    ("7891000400136", "Coxinha 4 unidades", "Lote304", "Casa", 1, "", 3.00, 10.00),
    
    # Cafés e bebidas quentes
    ("7891000500102", "Café Expresso", "Lote401", "Casa", 1, "", 1.00, 4.00),
    ("7891000500119", "Cappuccino", "Lote402", "Casa", 1, "", 2.00, 7.00),
    ("7891000500126", "Chocolate Quente", "Lote403", "Casa", 1, "", 2.50, 8.00),
]

try:
    # Inserir produtos
    for produto in produtos_exemplo:
        cursor.execute("""
            INSERT OR IGNORE INTO produtos 
            (codigo_barras, nome, lote, marca, tipo_quantidade_id, data_validade, preco_custo, preco_venda)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, produto)
    
    conn.commit()
    print(f"Adicionados {len(produtos_exemplo)} produtos de exemplo ao banco de dados!")
    
    # Verificar quantos produtos foram inseridos
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total_produtos = cursor.fetchone()[0]
    print(f"Total de produtos no banco: {total_produtos}")
    
except sqlite3.Error as e:
    print(f"Erro ao inserir produtos: {e}")
    conn.rollback()
finally:
    conn.close() 