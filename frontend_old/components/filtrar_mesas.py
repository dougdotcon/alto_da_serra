import flet as ft
import requests
from components.cards_mesas import gerar_cards_mesas

def filtrar_mesas(cards_mesas, filtros, mostrar_detalhes_fn, page):
    try:
        mesas = requests.get("http://127.0.0.1:8000/mesas").json()
        status_selecionados = [k for k, cb in filtros.items() if cb.value]
        cards_mesas.controls.clear()
        cards_mesas.controls.extend(
            gerar_cards_mesas(mesas, status_selecionados, mostrar_detalhes_fn)
        )
        page.update()
    except Exception as e:
        page.snack_bar = ft.SnackBar(
            ft.Text(f"Erro ao aplicar filtro: {str(e)}"),
            bgcolor=ft.Colors.RED_100
        )
        page.snack_bar.open = True
        page.update()
