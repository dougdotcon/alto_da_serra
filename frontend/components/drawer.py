import flet as ft
from datetime import datetime

def construir_drawer(nome_usuario, tipo_usuario, hora_text, page):
    botao_fechar_menu = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.CLOSE,
                icon_color=ft.Colors.RED,
                tooltip="Fechar menu",
                on_click=lambda _: (setattr(page.drawer, "open", False), page.update())
            )
        ],
        alignment=ft.MainAxisAlignment.END
    )

    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                width=260,
                padding=0,
                content=ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    padding=10,
                    content=ft.Column(
                        controls=[
                            ft.Stack([
                                ft.Container(
                                    content=ft.Image(
                                        src="logocliente.png",
                                        width=150,
                                        height=100,
                                        fit=ft.ImageFit.COVER
                                    ),
                                    border_radius=50,
                                    alignment=ft.alignment.center,
                                    clip_behavior=ft.ClipBehavior.HARD_EDGE
                                ),
                                ft.Container(
                                    content=botao_fechar_menu,
                                    alignment=ft.alignment.top_right
                                )
                            ]),
                            ft.Text(f"Usuário: {nome_usuario}", size=10, weight=ft.FontWeight.W_600),
                            ft.Text(f"Tipo: {tipo_usuario}", size=10),
                            ft.Text(f"Data: {datetime.now().strftime('%d/%m/%Y')}", size=11),
                            hora_text,
                            ft.Divider(),
                            ft.ElevatedButton("\U0001F4CB Mesas", on_click=lambda _: None, icon=ft.icons.TABLE_RESTAURANT),
                            ft.ElevatedButton("\U0001F4E6 Estoque", on_click=lambda _: None, icon=ft.icons.INVENTORY_2),
                            ft.ElevatedButton("\U0001F468\u200D\U0001F373 Cozinha", on_click=lambda _: None, icon=ft.icons.LUNCH_DINING, height=30),
                            ft.ElevatedButton("\U0001F4E6 Produtos", on_click=lambda _: None, icon=ft.icons.INVENTORY, height=30),
                            ft.Divider(),
                            ft.ElevatedButton("\U0001F6AA Sair", on_click=lambda _: page.go("/logout"), icon=ft.icons.LOGOUT)
                        ],
                        spacing=5,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            )
        ]
    )

    return drawer
