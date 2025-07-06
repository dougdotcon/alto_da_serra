import flet as ft
import requests

def handle_card_click(e, mesa, mostrar_detalhes_fn):
    """Handler para clique no card da mesa"""
    print(f"DEBUG: Card clicado para mesa: {mesa}")
    try:
        mostrar_detalhes_fn(mesa)
    except Exception as ex:
        print(f"DEBUG: Erro ao mostrar detalhes: {ex}")

def gerar_cards_mesas(mesas, status_selecionados, mostrar_detalhes):
    cards = []

    # Dicionário de cores por status
    cores_status = {
        "Livre": ft.Colors.GREEN_100,
        "Ocupada": ft.Colors.RED_100,
        "Reservada": ft.Colors.ORANGE_100,
        "Em Atendimento": ft.Colors.BLUE_100,
        "Aguardando Pagamento": ft.Colors.PURPLE_100,
        "Fechada": ft.Colors.GREY_100
    }

    for mesa in mesas:
        status = mesa["status"]

        # Aplica filtros de status
        if status_selecionados and status not in status_selecionados:
            continue

        cor_fundo = cores_status.get(status, ft.Colors.BLUE_100)

        cards.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(f"\U0001FA91 {mesa['nome']}", size=14, weight=ft.FontWeight.W_600),
                        ft.Text(f"Cliente: {mesa['cliente'] or '---'}", size=10),
                        ft.Text(f"Status: {mesa['status']}", size=10),
                        ft.Text(f"Total: R$ {mesa['total']:.2f}", size=10)
                    ], spacing=5),
                    padding=10,
                    border_radius=10,
                    bgcolor=cor_fundo,
                    on_click=lambda e, m=mesa: handle_card_click(e, m, mostrar_detalhes),
                    width=160,
                    height=120
                ),
                elevation=2
            )
        )

    return cards
