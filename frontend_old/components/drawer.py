import flet as ft
from datetime import datetime

def construir_drawer(nome_usuario, tipo_usuario, hora_text, page):
    """Constrói o drawer lateral"""
    
    # Botão de fechar
    close_button = ft.IconButton(
        icon=ft.Icons.CLOSE,
        icon_color=ft.Colors.RED,
        on_click=lambda _: setattr(page.drawer, "open", False)
    )
    
    # Cabeçalho do drawer
    drawer_header = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(f"Olá, {nome_usuario}", size=16, weight=ft.FontWeight.BOLD),
                close_button
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text(f"Tipo: {tipo_usuario}", size=12),
            hora_text
        ], spacing=5),
        padding=10
    )
    
    # Menu do drawer
    drawer_menu = ft.Container(
        content=ft.Column([
            ft.Text("Menu", size=14, weight=ft.FontWeight.BOLD),
            ft.Column([
                ft.ElevatedButton("\U0001F4CB Mesas", on_click=lambda _: None, icon=ft.Icons.TABLE_RESTAURANT),
                ft.ElevatedButton("\U0001F4E6 Estoque", on_click=lambda _: None, icon=ft.Icons.INVENTORY_2),
                ft.ElevatedButton("\U0001F468\u200D\U0001F373 Cozinha", on_click=lambda _: None, icon=ft.Icons.LUNCH_DINING, height=30),
                ft.ElevatedButton("\U0001F4E6 Produtos", on_click=lambda _: None, icon=ft.Icons.INVENTORY, height=30),
                ft.Divider(),
                ft.ElevatedButton("\U0001F6AA Sair",
                    icon=ft.Icons.LOGOUT,
                    icon_color=ft.Colors.RED,
                    on_click=lambda _: page.go("/logout"),
                    bgcolor=ft.Colors.WHITE
                )
            ],
            spacing=5,
            alignment=ft.MainAxisAlignment.START
            )
        ], spacing=20),
        padding=10
    )
    
    # Drawer completo
    return ft.NavigationDrawer(
        controls=[
            drawer_header,
            ft.Divider(),
            drawer_menu
        ]
    )