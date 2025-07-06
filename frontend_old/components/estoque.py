import flet as ft
import requests
from datetime import datetime

def criar_tela_estoque(page: ft.Page):
    """Cria a tela de gestão de estoque"""
    
    # Estados
    produtos = []
    
    # Campos de busca
    busca_input = ft.TextField(
        label="Buscar produto",
        width=300,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.GREY_50,
        prefix_icon=ft.Icons.SEARCH
    )
    
    # Tabela de estoque
    estoque_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Marca", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Lote", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Validade", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Preço Custo", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Preço Venda", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
    )
    
    # Mensagem de status
    status_message = ft.Text("", color=ft.Colors.GREEN, size=14)
    
    def carregar_produtos():
        """Carrega a lista de produtos para o estoque"""
        try:
            response = requests.get("http://127.0.0.1:8000/produtos")
            if response.status_code == 200:
                produtos.clear()
                produtos.extend(response.json())
                atualizar_tabela()
                mostrar_sucesso(f"Carregados {len(produtos)} produtos")
        except Exception as e:
            mostrar_erro(f"Erro ao carregar produtos: {str(e)}")
    
    def atualizar_tabela():
        """Atualiza a tabela de estoque"""
        estoque_table.rows.clear()
        
        # Filtrar produtos se houver busca
        produtos_filtrados = produtos
        if busca_input.value:
            termo = busca_input.value.lower()
            produtos_filtrados = [
                p for p in produtos 
                if termo in p["nome"].lower() or termo in p["codigo_barras"].lower()
            ]
        
        for produto in produtos_filtrados:
            # Determinar status baseado na validade
            status = "Disponível"
            status_color = ft.Colors.GREEN
            
            if produto["data_validade"]:
                try:
                    data_validade = datetime.strptime(produto["data_validade"], "%Y-%m-%d")
                    dias_restantes = (data_validade - datetime.now()).days
                    
                    if dias_restantes < 0:
                        status = "Vencido"
                        status_color = ft.Colors.RED
                    elif dias_restantes <= 30:
                        status = "Próximo ao vencimento"
                        status_color = ft.Colors.ORANGE
                except:
                    pass
            
            estoque_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(produto["codigo_barras"])),
                        ft.DataCell(ft.Text(produto["nome"])),
                        ft.DataCell(ft.Text(produto["marca"] or "-")),
                        ft.DataCell(ft.Text(produto["lote"] or "-")),
                        ft.DataCell(ft.Text(produto["data_validade"] or "-")),
                        ft.DataCell(ft.Text(f"R$ {produto['preco_custo']:.2f}")),
                        ft.DataCell(ft.Text(f"R$ {produto['preco_venda']:.2f}")),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(status, color=ft.Colors.WHITE, size=12),
                                bgcolor=status_color,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=12
                            )
                        )
                    ]
                )
            )
        page.update()
    
    def mostrar_sucesso(mensagem):
        """Mostra mensagem de sucesso"""
        status_message.value = mensagem
        status_message.color = ft.Colors.GREEN
        page.update()
    
    def mostrar_erro(mensagem):
        """Mostra mensagem de erro"""
        status_message.value = mensagem
        status_message.color = ft.Colors.RED
        page.update()
    
    def buscar_produtos(e):
        """Filtra produtos baseado na busca"""
        atualizar_tabela()
    
    def gerar_relatorio():
        """Gera relatório de estoque (placeholder)"""
        mostrar_erro("Funcionalidade de relatório em desenvolvimento")
    
    # Configurar eventos
    busca_input.on_change = buscar_produtos
    
    # Botões de ação
    btn_atualizar = ft.ElevatedButton(
        text="Atualizar",
        icon=ft.Icons.REFRESH,
        on_click=lambda e: carregar_produtos(),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            padding=ft.padding.all(15)
        )
    )
    
    btn_relatorio = ft.ElevatedButton(
        text="Gerar Relatório",
        icon=ft.Icons.DESCRIPTION,
        on_click=lambda e: gerar_relatorio(),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
            padding=ft.padding.all(15)
        )
    )
    
    btn_limpar_busca = ft.ElevatedButton(
        text="Limpar Busca",
        icon=ft.Icons.CLEAR,
        on_click=lambda e: (setattr(busca_input, 'value', ''), atualizar_tabela()),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREY,
            color=ft.Colors.WHITE,
            padding=ft.padding.all(15)
        )
    )
    
    # Estatísticas
    def calcular_estatisticas():
        """Calcula estatísticas do estoque"""
        total_produtos = len(produtos)
        produtos_vencidos = 0
        produtos_vencendo = 0
        valor_total = 0
        
        for produto in produtos:
            valor_total += produto["preco_custo"]
            
            if produto["data_validade"]:
                try:
                    data_validade = datetime.strptime(produto["data_validade"], "%Y-%m-%d")
                    dias_restantes = (data_validade - datetime.now()).days
                    
                    if dias_restantes < 0:
                        produtos_vencidos += 1
                    elif dias_restantes <= 30:
                        produtos_vencendo += 1
                except:
                    pass
        
        return {
            "total": total_produtos,
            "vencidos": produtos_vencidos,
            "vencendo": produtos_vencendo,
            "valor_total": valor_total
        }
    
    def criar_card_estatistica(titulo, valor, cor, icone):
        """Cria um card de estatística"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(icone, color=cor, size=30),
                        ft.Text(titulo, size=14, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Text(str(valor), size=24, weight=ft.FontWeight.BOLD, color=cor)
                ], spacing=10),
                padding=15,
                width=200
            ),
            elevation=2
        )
    
    # Inicializar dados
    carregar_produtos()
    
    # Layout principal
    return ft.Container(
        content=ft.Column([
            # Título
            ft.Container(
                content=ft.Text(
                    "Gestão de Estoque",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900
                ),
                padding=ft.padding.only(bottom=20)
            ),
            
            # Estatísticas
            ft.Container(
                content=ft.Row([
                    criar_card_estatistica("Total de Produtos", len(produtos), ft.Colors.BLUE, ft.Icons.INVENTORY),
                    criar_card_estatistica("Produtos Vencidos", 0, ft.Colors.RED, ft.Icons.WARNING),
                    criar_card_estatistica("Próximos ao Vencimento", 0, ft.Colors.ORANGE, ft.Icons.SCHEDULE),
                    criar_card_estatistica("Valor Total", f"R$ {sum(p['preco_custo'] for p in produtos):.2f}", ft.Colors.GREEN, ft.Icons.ATTACH_MONEY),
                ], wrap=True, spacing=10),
                padding=ft.padding.only(bottom=20)
            ),
            
            # Controles
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            busca_input,
                            btn_limpar_busca,
                            btn_atualizar,
                            btn_relatorio
                        ], wrap=True, spacing=10),
                        status_message
                    ], spacing=15),
                    padding=20
                ),
                elevation=2
            ),
            
            # Tabela
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Produtos em Estoque", size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Container(
                            content=estoque_table,
                            scroll=ft.ScrollMode.AUTO
                        )
                    ], spacing=15),
                    padding=20
                ),
                elevation=2
            )
        ], spacing=20, scroll=ft.ScrollMode.AUTO),
        padding=20,
        expand=True
    ) 