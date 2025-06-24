import flet as ft
import requests
from painel import painel_view

def main(page: ft.Page):
    page.title = "SCMP LIM Soluções"
    page.bgcolor = ft.Colors.WHITE
    page.window_icon_url = "logofornecedor.png"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    email = ft.TextField(label="Usuário", width=300)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)
    mensagem = ft.Text(value="", color=ft.Colors.RED)
    logo = ft.Image(src="logofornecedor.png", width=150)

    def entrar_click(e):
        try:
            res = requests.post("http://127.0.0.1:8000/login", json={
                "email": email.value,
                "password": senha.value
            })
            if res.status_code == 200:
                data = res.json()
                mensagem.value = "Credenciais válidas"
                mensagem.color = ft.Colors.GREEN

                page.client_storage.set("autenticado", True)
                page.client_storage.set("usuario_nome", data["nome"])
                page.client_storage.set("usuario_tipo", data["tipo"])
                page.client_storage.set("usuario_user", data["user"])

                page.go("/painel")

            else:
                mensagem.value = "Credenciais inválidas"
                mensagem.color = ft.Colors.RED
                page.update()
        except Exception as err:
            mensagem.value = f"Erro ao conectar: {err}"
            mensagem.color = ft.Colors.RED
            page.update()

    def login_view():
        return ft.View(
            route="/login",
            controls=[
                ft.Column(
                    controls=[
                        logo,
                        ft.Text("SCMP LIM Soluções", size=24),
                        email,
                        senha,
                        ft.ElevatedButton("Entrar", on_click=entrar_click, width=300),
                        mensagem
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def route_change(route):
        autenticado = page.client_storage.get("autenticado") or False
        rota = route.route
        page.views.clear()

        if rota == "/logout":
            page.client_storage.clear()
            page.go("/login")
            return

        if rota == "/painel":
            if not autenticado:
                page.go("/login")
                return

            nome = page.client_storage.get("usuario_nome") or ""
            tipo = page.client_storage.get("usuario_tipo") or ""
            user = page.client_storage.get("usuario_user") or ""
            print(user)
            page.views.append(painel_view(page, nome_usuario=nome, tipo_usuario=tipo, user_id=user))

        else:
            page.views.append(login_view())

        page.update()

    page.on_route_change = route_change
    page.go("/login")

if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        assets_dir="assets"
    )
