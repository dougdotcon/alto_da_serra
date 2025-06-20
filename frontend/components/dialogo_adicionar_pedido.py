import flet as ft
import requests

# Função para buscar produtos via API
def buscar_produtos():
    url = "http://127.0.0.1:8000/produtos"  # A URL da API onde os produtos são listados
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()  # Retorna a lista de produtos (id, nome, preco)
    else:
        return []

def abrir_dialogo_adicionar_pedido(page, mesa_id, callback):
    print(f"Abrindo o diálogo de adicionar pedido para a mesa {mesa_id}...")

    # Buscar os produtos via API
    produtos = buscar_produtos()

    if not produtos:
        page.snack_bar = ft.SnackBar(ft.Text("Erro ao carregar produtos."))
        page.snack_bar.open = True
        page.update()
        return

    # Criando as opções para o Dropdown
    dropdown_options = []
    for produto in produtos:
        # Criando a opção com o nome e o preço
        option = ft.dropdown.Option(f"[{produto['id']}] - {produto['nome']} - R$ {produto['preco']:.2f}")
        dropdown_options.append(option)

    # Função para calcular o total
    def calcular_total(e):
        try:
            quantidade = int(quantidade_input.value)  # Obtém a quantidade (somente números)
            produto_selecionado = produto_dropdown.value  # Obtém o texto do produto selecionado
            print(produto_selecionado)
            # Extraímos o ID entre os colchetes
            produto_id = int(produto_selecionado.split('[')[1].split(']')[0])
            # Agora, encontramos o preço do produto pelo ID
            preco_unitario = next(p['preco'] for p in produtos if p['id'] == produto_id)
            total = preco_unitario * quantidade  # Calcula o total
            total_text.value = f"Total: R$ {total:.2f}"
            page.update()
        except ValueError:
            total_text.value = "Quantidade inválida. Insira um número."
            page.update()

    def cancelar(e):
        print("Cancelando o diálogo de adicionar pedido...")
        page.dialog.open = False  # Fecha o diálogo de adicionar pedido
        page.update()  # Atualiza a página para refletir a remoção
        callback()  # Chama o callback após o fechamento do diálogo

    def adicionar(e):
        print("Pedido adicionado!")
        page.snack_bar = ft.SnackBar(ft.Text("Pedido adicionado com sucesso!"))
        page.snack_bar.open = True
        page.overlay.remove(dialogo_adicionar)  # Remove o diálogo de adicionar pedido
        page.update()  # Atualiza a página para refletir a remoção
        callback()  # Chama o callback após o fechamento do diálogo

    # Criando o conteúdo para o diálogo de adicionar pedido (exemplo de dropdown e campo de texto)
    conteudo = ft.Column([
        ft.Text("Selecione o produto", size=14),
        produto_dropdown := ft.Dropdown(
            options=dropdown_options,  # Preenche o dropdown com os produtos da API
            width=300,
            height=50,
            text_style=ft.TextStyle(size=10),
            on_change=calcular_total
        ),
        ft.Text("Quantidade", size=14),
        quantidade_input := ft.TextField(
            label="Quantidade", 
            width=150, 
            height=40, 
            keyboard_type=ft.KeyboardType.NUMBER,  # Somente números
            on_change=calcular_total  # Atualiza o total quando a quantidade muda
        ),
        total_text := ft.Text("Total: R$ 0.00", size=14, weight=ft.FontWeight.BOLD)
    ], spacing=10)

    # Adicionando padding no Container que envolve o conteúdo
    container_conteudo = ft.Container(
        content=conteudo,
        width=400,  # Largura do conteúdo
        height=300,  # Altura do conteúdo
        padding=20  # Padding para o conteúdo ficar com espaço
    )

    # Criando o diálogo de adicionar pedido com o conteúdo acima
    dialogo_adicionar = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Adicionar Pedido - Mesa {mesa_id}"),
        content=container_conteudo,
        actions=[
            ft.TextButton("Cancelar", on_click=cancelar),  # Ação para cancelar
            ft.TextButton("Adicionar", on_click=adicionar)  # Ação para adicionar
        ],
        on_dismiss=lambda e: page.overlay.remove(dialogo_adicionar)  # Remover o diálogo quando for fechado
    )

    # Adicionando o diálogo de adicionar pedido ao overlay da página
    page.dialog = dialogo_adicionar
    page.dialog.open = True  # Usando o overlay para mostrar o diálogo acima de outros
    page.update()  # Força a atualização da página para mostrar o diálogo
    print(f"Diálogo de adicionar pedido para a mesa {mesa_id} adicionado ao overlay.")
