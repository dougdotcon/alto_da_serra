import flet as ft
from datetime import datetime
import time
import threading
import requests
from components.painel_controller import inicializar_painel_components
from components.filtros import criar_filtros
from components.filtros import criar_filtros
from components.detalhes_mesa import mostrar_detalhes
from components.drawer import construir_drawer
from components.cards_mesas import gerar_cards_mesas
from components.filtro_abertura import construir_filtro_e_abertura, construir_inputs_abertura
from components.relogio import construir_relogio
from components.filtrar_mesas import filtrar_mesas

def painel_view(page: ft.Page, nome_usuario: str = "", tipo_usuario: str = "", user_id: str = "", login_user: str = ""):
    try:
        config = requests.get("http://127.0.0.1:8000/configuracao").json()
        qtd_mesas = config.get("mesas", 0)
    except Exception as e:
        qtd_mesas = 0
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao carregar configuração: {str(e)}"), bgcolor=ft.Colors.RED_100)
        page.snack_bar.open = True
        page.update()

    mesas = requests.get("http://127.0.0.1:8000/mesas").json()

    hora_text = construir_relogio(page)

    mostrar_detalhes_fn = lambda m: mostrar_detalhes(m, page)

    filtros, mesa_id_input, cliente_input, status_dropdown, cards_mesas, aplicar_filtro = inicializar_painel_components(
        page, mostrar_detalhes_fn
    )

    drawer = construir_drawer(nome_usuario, tipo_usuario, hora_text, page)

    app_bar = ft.AppBar(
        title=ft.Text("Sistema de Controle de Mesas e Pedidos", size=18, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.Colors.BLUE_50,
        leading=ft.IconButton(icon=ft.Icons.MENU, on_click=lambda _: (setattr(page, "drawer", drawer), setattr(page.drawer, "open", True), page.update())),
        actions=[ft.IconButton(icon=ft.Icons.SEARCH)]
    )

    filtro_e_abertura = construir_filtro_e_abertura(
        filtros, user_id, page, mesa_id_input, cliente_input, status_dropdown, aplicar_filtro
    )

    return ft.View(
        route="/painel",
        controls=[
            ft.Container(
                content=ft.Column([
                    filtro_e_abertura,
                    cards_mesas
                ], scroll=ft.ScrollMode.AUTO, spacing=20),
                expand=2,
                padding=20
            )
        ],
        appbar=app_bar,
        drawer=drawer,
        scroll=ft.ScrollMode.AUTO
    )
