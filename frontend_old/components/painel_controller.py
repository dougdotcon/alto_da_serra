import flet as ft
import requests
from .filtros import criar_filtros
from .filtro_abertura import construir_inputs_abertura
from .cards_mesas import gerar_cards_mesas

def inicializar_painel_components(page, mostrar_detalhes_fn):
    """Inicializa os componentes do painel"""
    
    # Construir filtros
    filtros = criar_filtros(lambda: aplicar_filtro())
    
    # Construir inputs de abertura
    mesa_id_input, cliente_input, status_dropdown = construir_inputs_abertura()
    
    # Container para os cards das mesas
    cards_mesas = ft.Container(
        content=ft.Row(
            controls=[],
            wrap=True,
            spacing=10,
            run_spacing=10,
            scroll=ft.ScrollMode.AUTO
        ),
        padding=10,
        expand=True
    )
    
    def aplicar_filtro():
        """Aplica os filtros selecionados"""
        try:
            # Obter status selecionados
            status_selecionados = [
                status for status, checkbox in filtros.items()
                if checkbox.value
            ]
            
            # Buscar mesas da API
            response = requests.get("http://127.0.0.1:8000/mesas")
            if response.status_code == 200:
                mesas = response.json()
                
                # Gerar cards das mesas
                cards = gerar_cards_mesas(mesas, status_selecionados, mostrar_detalhes_fn)
                
                # Atualizar container
                cards_mesas.content.controls = cards
                page.update()
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text(f"Erro ao buscar mesas: {response.status_code}"),
                    bgcolor=ft.Colors.RED_100
                )
                page.snack_bar.open = True
                page.update()
                
        except Exception as e:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro ao aplicar filtro: {str(e)}"),
                bgcolor=ft.Colors.RED_100
            )
            page.snack_bar.open = True
            page.update()
    
    # Aplicar filtro inicial
    aplicar_filtro()
    
    return filtros, mesa_id_input, cliente_input, status_dropdown, cards_mesas, aplicar_filtro
