import sqlite3

def atualizar_status_mesas():
    """Atualiza a base de dados para incluir o status 'Livre' e reorganizar os status"""
    try:
        conn = sqlite3.connect("restaurante.db")
        cursor = conn.cursor()

        # Verificar se o status 'Livre' já existe
        cursor.execute("SELECT COUNT(*) FROM status_mesas WHERE status = 'Livre'")
        livre_exists = cursor.fetchone()[0] > 0

        if not livre_exists:
            print("Adicionando status 'Livre'...")
            # Inserir o status 'Livre' no início
            cursor.execute("INSERT INTO status_mesas (status) VALUES ('Livre')")
            
            # Reordenar os IDs para ter: 1=Livre, 2=Aberto, 3=Fechada, 4=Reservada
            cursor.execute("UPDATE status_mesas SET id = id + 10 WHERE status != 'Livre'")
            
            # Atualizar para a nova ordem
            cursor.execute("UPDATE status_mesas SET id = 1 WHERE status = 'Livre'")
            cursor.execute("UPDATE status_mesas SET id = 2 WHERE status = 'Aberto'")
            cursor.execute("UPDATE status_mesas SET id = 3 WHERE status = 'Fechada'")
            cursor.execute("UPDATE status_mesas SET id = 4 WHERE status = 'Reservada'")
            
            print("Status 'Livre' adicionado com sucesso!")
        else:
            print("Status 'Livre' já existe na base de dados.")

        # Atualizar todas as mesas que estão com status "Aberto" para "Livre"
        cursor.execute("""
            UPDATE mesas 
            SET status_id = (SELECT id FROM status_mesas WHERE status = 'Livre')
            WHERE status_id = (SELECT id FROM status_mesas WHERE status = 'Aberto')
            AND cliente IS NULL
        """)
        
        mesas_atualizadas = cursor.rowcount
        if mesas_atualizadas > 0:
            print(f"{mesas_atualizadas} mesas foram atualizadas de 'Aberto' para 'Livre'.")

        # Verificar a estrutura atual
        print("\nStatus disponíveis após atualização:")
        cursor.execute("SELECT id, status FROM status_mesas ORDER BY id")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]}")

        print("\nDistribuição de mesas por status:")
        cursor.execute("""
            SELECT s.status, COUNT(m.id) as quantidade
            FROM status_mesas s
            LEFT JOIN mesas m ON s.id = m.status_id
            GROUP BY s.id, s.status
            ORDER BY s.id
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} mesa(s)")

        conn.commit()
        conn.close()
        print("\nAtualização concluída com sucesso!")

    except Exception as e:
        print(f"Erro ao atualizar status das mesas: {str(e)}")

if __name__ == "__main__":
    atualizar_status_mesas()
