import flet as ft
import requests
from components.filtros import criar_filtros
from components.filtro_abertura import construir_inputs_abertura
from components.cards_mesas import gerar_cards_mesas

def inicializar_painel_components(page, mostrar_detalhes_fn):
    mesa_id_input, cliente_input, status_dropdown = construir_inputs_abertura()
    cards_mesas = ft.Row(wrap=True, spacing=10)

    filtros = criar_filtros(lambda: aplicar_filtro())

    def aplicar_filtro():
        nonlocal filtros
        try:
            mesas = requests.get("http://127.0.0.1:8000/mesas").json()
            status_selecionados = [k for k, cb in filtros.items() if cb.value]
            cards_mesas.controls.clear()
            cards_mesas.controls.extend(
                gerar_cards_mesas(mesas, status_selecionados, mostrar_detalhes_fn)
            )
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao aplicar filtro: {str(e)}"), bgcolor=ft.Colors.RED_100)
            page.snack_bar.open = True
            page.update()

    aplicar_filtro()

    return filtros, mesa_id_input, cliente_input, status_dropdown, cards_mesas, aplicar_filtro
