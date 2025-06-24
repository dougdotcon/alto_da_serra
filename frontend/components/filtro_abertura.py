import flet as ft
from .abertura_mesa import construir_abertura_mesa

def construir_inputs_abertura():
    mesa_id_input = ft.TextField(label="ID da Mesa", width=200, height=40, text_style=ft.TextStyle(size=10))
    cliente_input = ft.TextField(label="Nome do Cliente", width=250, height=40, text_style=ft.TextStyle(size=10))
    status_dropdown = ft.Dropdown(
        label="Novo Status",
        options=[ft.dropdown.Option("Aberta"), ft.dropdown.Option("Reservada")],
        width=200,
        value="Aberta"
    )
    return mesa_id_input, cliente_input, status_dropdown

def construir_filtro_e_abertura(filtros, user_id, page, mesa_id_input, cliente_input, status_dropdown, aplicar_filtro):
    return ft.Card(
        elevation=1,
        margin=10,
        content=ft.Container(
            padding=10,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            content=ft.ExpansionTile(
                title=ft.Text("\U0001F50D Filtros e Abertura de Mesas", size=12, weight=ft.FontWeight.W_600),
                initially_expanded=False,
                controls=[
                    ft.ResponsiveRow(
                        columns=12,
                        controls=[
                            ft.Container(
                                col={"sm": 12, "md": 6},
                                content=ft.Column(
                                    spacing=4,
                                    controls=[
                                        ft.Text("Filtros de Mesas", size=11, weight=ft.FontWeight.W_500),
                                        *filtros.values()
                                    ]
                                )
                            ),
                            ft.Container(
                                col={"sm": 12, "md": 6},
                                content=ft.Container(
                                    content=construir_abertura_mesa(
                                        user_id,
                                        page,
                                        mesa_id_input,
                                        cliente_input,
                                        status_dropdown,
                                        aplicar_filtro
                                    ),
                                    margin=ft.margin.only(bottom=10)
                                )
                            )
                        ]
                    )
                ]
            )
        )
    )
