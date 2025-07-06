import flet as ft
import requests
from datetime import datetime

def criar_tela_produtos(page: ft.Page):
    """Cria a tela de gestão de produtos"""
    
    # Estados
    produtos = []
    tipos_quantidade = []
    
    # Campos do formulário
    codigo_barras_input = ft.TextField(
        label="Código de Barras",
        width=200,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.GREY_50
    )
    
    nome_input = ft.TextField(
        label="Nome do Produto",
        width=300,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.GREY_50
    )
    
    lote_input = ft.TextField(
        label="Lote",
        width=150,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.GREY_50
    )
    
    marca_input = ft.TextField(
        label="Marca",
        width=200,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.GREY_50
    )
    
    tipo_dropdown = ft.Dropdown(
        label="Tipo de Quantidade",
        width=200,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.GREY_50
    )
    
    data_validade_input = ft.TextField(
        label="Data de Validade (YYYY-MM-DD)",
        width=200,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.GREY_50
    )
    
    preco_custo_input = ft.TextField(
        label="Preço de Custo",
        width=150,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.GREY_50
    )
    
    preco_venda_input = ft.TextField(
        label="Preço de Venda",
        width=150,
        border_radius=8,
        filled=True,
        bgcolor=ft.Colors.GREY_50
    )
    
    # Tabela de produtos
    produtos_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Marca", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Preço Custo", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Preço Venda", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_200),
    )
    
    # Mensagem de status
    status_message = ft.Text("", color=ft.Colors.GREEN, size=14)
    
    def carregar_tipos_quantidade():
        """Carrega os tipos de quantidade disponíveis"""
        try:
            response = requests.get("http://127.0.0.1:8000/tipos_quantidade")
            if response.status_code == 200:
                tipos_quantidade.clear()
                tipos_quantidade.extend(response.json())
                tipo_dropdown.options = [
                    ft.dropdown.Option(key=str(tipo["id"]), text=tipo["nome"])
                    for tipo in tipos_quantidade
                ]
                page.update()
        except Exception as e:
            mostrar_erro(f"Erro ao carregar tipos de quantidade: {str(e)}")
    
    def carregar_produtos():
        """Carrega a lista de produtos"""
        try:
            response = requests.get("http://127.0.0.1:8000/produtos")
            if response.status_code == 200:
                produtos.clear()
                produtos.extend(response.json())
                atualizar_tabela()
        except Exception as e:
            mostrar_erro(f"Erro ao carregar produtos: {str(e)}")
    
    def atualizar_tabela():
        """Atualiza a tabela de produtos"""
        produtos_table.rows.clear()
        for produto in produtos:
            produtos_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(produto["codigo_barras"])),
                        ft.DataCell(ft.Text(produto["nome"])),
                        ft.DataCell(ft.Text(produto["marca"])),
                        ft.DataCell(ft.Text(produto["tipo_quantidade"])),
                        ft.DataCell(ft.Text(f"R$ {produto['preco_custo']:.2f}")),
                        ft.DataCell(ft.Text(f"R$ {produto['preco_venda']:.2f}")),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar",
                                    icon_color=ft.Colors.BLUE,
                                    on_click=lambda e, p=produto: editar_produto(p)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Excluir",
                                    icon_color=ft.Colors.RED,
                                    on_click=lambda e, p=produto: confirmar_exclusao(p)
                                )
                            ])
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
    
    def limpar_formulario():
        """Limpa todos os campos do formulário"""
        codigo_barras_input.value = ""
        nome_input.value = ""
        lote_input.value = ""
        marca_input.value = ""
        tipo_dropdown.value = None
        data_validade_input.value = ""
        preco_custo_input.value = ""
        preco_venda_input.value = ""
        page.update()
    
    def adicionar_produto(e):
        """Adiciona um novo produto"""
        try:
            if not all([codigo_barras_input.value, nome_input.value, tipo_dropdown.value,
                       preco_custo_input.value, preco_venda_input.value]):
                mostrar_erro("Preencha todos os campos obrigatórios")
                return
            
            produto_data = {
                "codigo_barras": codigo_barras_input.value,
                "nome": nome_input.value,
                "lote": lote_input.value or "",
                "marca": marca_input.value or "",
                "tipo_quantidade_id": int(tipo_dropdown.value),
                "data_validade": data_validade_input.value or "",
                "preco_custo": float(preco_custo_input.value),
                "preco_venda": float(preco_venda_input.value)
            }
            
            response = requests.post("http://127.0.0.1:8000/produtos", json=produto_data)
            if response.status_code == 200:
                mostrar_sucesso("Produto adicionado com sucesso!")
                limpar_formulario()
                carregar_produtos()
            else:
                mostrar_erro(f"Erro ao adicionar produto: {response.json().get('detail', 'Erro desconhecido')}")
        
        except ValueError:
            mostrar_erro("Verifique os valores numéricos inseridos")
        except Exception as e:
            mostrar_erro(f"Erro ao adicionar produto: {str(e)}")
    
    def editar_produto(produto):
        """Edita um produto (placeholder)"""
        mostrar_erro("Funcionalidade de edição em desenvolvimento")
    
    def confirmar_exclusao(produto):
        """Confirma exclusão de produto (placeholder)"""
        mostrar_erro("Funcionalidade de exclusão em desenvolvimento")
    
    # Botões de ação
    btn_adicionar = ft.ElevatedButton(
        text="Adicionar Produto",
        icon=ft.Icons.ADD,
        on_click=adicionar_produto,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            padding=ft.padding.all(15)
        )
    )
    
    btn_limpar = ft.ElevatedButton(
        text="Limpar",
        icon=ft.Icons.CLEAR,
        on_click=lambda e: limpar_formulario(),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREY,
            color=ft.Colors.WHITE,
            padding=ft.padding.all(15)
        )
    )
    
    btn_atualizar = ft.ElevatedButton(
        text="Atualizar Lista",
        icon=ft.Icons.REFRESH,
        on_click=lambda e: carregar_produtos(),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
            padding=ft.padding.all(15)
        )
    )
    
    # Inicializar dados
    carregar_tipos_quantidade()
    carregar_produtos()
    
    # Layout principal
    return ft.Container(
        content=ft.Column([
            # Título
            ft.Container(
                content=ft.Text(
                    "Gestão de Produtos",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900
                ),
                padding=ft.padding.only(bottom=20)
            ),
            
            # Formulário
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Adicionar Novo Produto", size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        
                        # Linha 1
                        ft.Row([
                            codigo_barras_input,
                            nome_input,
                            marca_input
                        ], wrap=True, spacing=10),
                        
                        # Linha 2
                        ft.Row([
                            lote_input,
                            tipo_dropdown,
                            data_validade_input
                        ], wrap=True, spacing=10),
                        
                        # Linha 3
                        ft.Row([
                            preco_custo_input,
                            preco_venda_input
                        ], wrap=True, spacing=10),
                        
                        # Botões
                        ft.Row([
                            btn_adicionar,
                            btn_limpar,
                            btn_atualizar
                        ], spacing=10),
                        
                        # Status
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
                        ft.Text("Lista de Produtos", size=18, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Container(
                            content=produtos_table,
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