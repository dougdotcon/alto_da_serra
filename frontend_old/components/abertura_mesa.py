import flet as ft
import requests

def construir_abertura_mesa(user_id, page, mesa_id_input, cliente_input, status_dropdown, aplicar_filtro):
    def abrir_mesa(e):
        id_mesa = mesa_id_input.value.strip()
        nome = cliente_input.value.strip()
        status = status_dropdown.value

        if id_mesa.isdigit() and nome and status:
            id_mesa = int(id_mesa)
            try:
                response = requests.post("http://127.0.0.1:8000/atualizar_mesa", json={
                    "user_id": user_id,
                    "id": id_mesa,
                    "cliente": nome,
                    "status": status
                })

                if response.status_code == 200:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Mesa {id_mesa} atualizada para {nome} ({status})"))
                    page.snack_bar.open = True
                    aplicar_filtro()
                    return
                else:
                    try:
                        erro_detail = response.json().get("detail", "Erro desconhecido.")
                    except Exception:
                        erro_detail = response.text
                    page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao atualizar mesa: {response.status_code} - {erro_detail}"))
                    page.snack_bar.open = True
                    page.update()
            except Exception as err:
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao atualizar mesa: {err}"))
                page.snack_bar.open = True
                page.update()

    return ft.Column(
        spacing=6,
        controls=[
            ft.Text("Abrir mesa por ID", size=11, weight=ft.FontWeight.W_500),
            ft.Container(
                margin=ft.margin.only(bottom=10),
                content=ft.ResponsiveRow(
                    controls=[
                        ft.Container(content=mesa_id_input, col={"sm": 12, "md": 6}),
                        ft.Container(content=cliente_input, col={"sm": 12, "md": 6}),
                    ],
                    spacing=10
                )
            ),
            ft.ResponsiveRow(
                controls=[
                    ft.Container(content=status_dropdown, col={"sm": 12, "md": 6}),
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Abrir Mesa",
                            icon=ft.Icons.ADD,
                            on_click=abrir_mesa,
                            height=35,
                            width=100,
                            style=ft.ButtonStyle(padding=10)
                        ),
                        col={"sm": 12, "md": 6}
                    )
                ],
                spacing=20
            )
        ]
    )
