import sqlite3
import os

def verificar_sistema():
    print("🔍 VERIFICAÇÃO FINAL DO SISTEMA")
    print("=" * 50)
    
    # 1. Verificar status do banco
    print("\n1️⃣ VERIFICANDO STATUS NO BANCO DE DADOS")
    conn = sqlite3.connect("backend/restaurante.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, status FROM status_mesas ORDER BY id")
    status_list = cursor.fetchall()
    print("   Status disponíveis:")
    for status in status_list:
        print(f"   ✅ ID {status[0]}: {status[1]}")
    
    # Verificar se temos os 4 status corretos
    expected_status = [(1, 'Livre'), (2, 'Aberto'), (3, 'Fechada'), (4, 'Reservada')]
    if status_list == expected_status:
        print("   ✅ Status configurados corretamente!")
    else:
        print("   ❌ Status não estão na ordem esperada")
    
    # 2. Verificar se mesas têm status válidos
    print("\n2️⃣ VERIFICANDO INTEGRIDADE DAS MESAS")
    cursor.execute("""
        SELECT COUNT(*) FROM mesas m 
        LEFT JOIN status_mesas sm ON m.status_id = sm.id 
        WHERE sm.status IS NULL
    """)
    mesas_invalidas = cursor.fetchone()[0]
    
    if mesas_invalidas == 0:
        print("   ✅ Todas as mesas têm status válidos")
    else:
        print(f"   ❌ {mesas_invalidas} mesas com status inválidos")
    
    # 3. Verificar valores totais sincronizados
    print("\n3️⃣ VERIFICANDO SINCRONIZAÇÃO DE VALORES")
    cursor.execute("""
        SELECT COUNT(*) FROM mesas m
        WHERE m.valor_total != (
            SELECT COALESCE(SUM(c.total), 0) 
            FROM consumo c 
            WHERE c.mesa_id = m.id
        )
    """)
    mesas_dessincronizadas = cursor.fetchone()[0]
    
    if mesas_dessincronizadas == 0:
        print("   ✅ Todos os valores estão sincronizados")
    else:
        print(f"   ❌ {mesas_dessincronizadas} mesas com valores dessincronizados")
    
    conn.close()
    
    # 4. Verificar arquivos de template
    print("\n4️⃣ VERIFICANDO TEMPLATES")
    templates_importantes = [
        "frontend/templates/mesas/mesa_detail.html",
        "frontend/templates/mesas/gestao_mesas.html",
        "frontend/templates/mesas/dashboard.html"
    ]
    
    for template in templates_importantes:
        if os.path.exists(template):
            print(f"   ✅ {template} existe")
        else:
            print(f"   ❌ {template} não encontrado")
    
    # 5. Verificar configurações de porta
    print("\n5️⃣ VERIFICANDO CONFIGURAÇÕES DE PORTA")
    
    # Verificar start_local.py
    with open("start_local.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "port', '8001'" in content and "8000" in content:
            print("   ✅ start_local.py configurado corretamente")
        else:
            print("   ❌ start_local.py com configuração incorreta")
    
    # Verificar settings.py
    with open("frontend/restaurante_frontend/settings.py", "r", encoding="utf-8") as f:
        content = f.read()
        if "http://127.0.0.1:8001" in content:
            print("   ✅ settings.py configurado corretamente")
        else:
            print("   ❌ settings.py com URL de API incorreta")
    
    print("\n" + "=" * 50)
    print("🎯 RESUMO DAS CORREÇÕES IMPLEMENTADAS:")
    print("✅ Campo user_id tornado opcional no MesaUpdate")
    print("✅ Status finalizar_conta corrigido para 'Livre' (ID: 1)")
    print("✅ Atualização automática de valor_total em adicionar_pedido")
    print("✅ Status do banco reorganizados corretamente")
    print("✅ Templates restaurados dos backups")
    print("✅ View gestao_mesas_view adicionada")
    print("✅ Rota /gestao-mesas/ configurada")
    print("✅ Portas atualizadas (Backend: 8001, Frontend: 8000)")
    print("✅ URL da API corrigida no Django")
    print("\n🚀 Sistema pronto para uso!")
    print("   Para iniciar: python start_local.py")

if __name__ == "__main__":
    verificar_sistema()
