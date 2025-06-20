# utils/consumo_utils.py
import flet as ft
import requests

def montar_itens_consumidos(page, mesa, controler_excluir_pedido, controler_pagar_item):
    try:
        response = requests.get(f"http://127.0.0.1:8000/consumo/{mesa['id']}")
        response.raise_for_status()
        itens = response.json()
    except Exception as err:
        itens = []
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao buscar itens: {err}"),
            bgcolor=ft.Colors.RED_100
        )
        page.snack_bar.open = True
        page.update()
        return [], None, 0

    total_geral = sum(item["preco"] * item["quantidade"] for item in itens)

    header = ft.Row([
        ft.Text("ID", expand=1, weight=ft.FontWeight.BOLD),
        ft.Text("Item", expand=3, weight=ft.FontWeight.BOLD),
        ft.Text("Preço", expand=2, weight=ft.FontWeight.BOLD),
        ft.Text("Qtd", expand=1, weight=ft.FontWeight.BOLD),
        ft.Text("Total", expand=2, weight=ft.FontWeight.BOLD),
        ft.Text("Ações", expand=2, weight=ft.FontWeight.BOLD),
    ], spacing=10)

    linhas = []
    for item in itens:
        total_item = item["preco"] * item["quantidade"]
        linhas.append(
            ft.Row([
                ft.Text(str(item["id"]), expand=1),
                ft.Text(item["nome"], expand=3),
                ft.Text(f"R$ {item['preco']:.2f}", expand=2),
                ft.Text(str(item["quantidade"]), expand=1),
                ft.Text(f"R$ {total_item:.2f}", expand=2),
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.DELETE, icon_color=ft.Colors.RED, tooltip="Excluir",
                        on_click=lambda e, id=item["id"]: controler_excluir_pedido(page, mesa,item["id"])
                    ),
                    ft.IconButton(
                        icon=ft.icons.ATTACH_MONEY, icon_color=ft.Colors.GREEN, tooltip="Pagar item",
                        on_click=lambda e, id=item["id"]: controler_pagar_item(page, mesa,item["id"])
                    )
                ], expand=2)
            ], spacing=10)
        )

    return linhas, header, total_geral
