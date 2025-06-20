import flet as ft
import requests

def gerar_cards_mesas(mesas, status_selecionados, mostrar_detalhes):
    cards = []

    # Mapeamento de cores por status
    cores_status = {
        "aberta": "#d4f8d4",     # Verde bem claro
        "fechada": "#f8d4d4",    # Vermelho bem claro
        "reservada": "#fff9c4"   # Amarelo bem claro
    }

    for mesa in mesas:
        status = mesa["status"].lower()

        if any(status == s.lower() for s in status_selecionados):
            cor_fundo = cores_status.get(status, ft.Colors.BLUE_100)

            cards.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(f"\U0001FA91 {mesa['nome']}", size=14, weight=ft.FontWeight.W_600),
                            ft.Text(f"Cliente: {mesa['cliente'] or '---'}", size=10),
                            ft.Text(f"Status: {mesa['status']}", size=10),
                            ft.Text(f"Total: R$ {mesa['total']:.2f}", size=10)
                        ]),
                        padding=10,
                        border_radius=10,
                        bgcolor=cor_fundo,
                        on_click=lambda e, m=mesa: mostrar_detalhes(m)
                    ),
                    width=160
                )
            )

    return cards
