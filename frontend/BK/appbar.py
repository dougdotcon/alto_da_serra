app_bar = ft.AppBar(
        title=ft.Text("My Flet", size=18, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.LinearGradient(
            begin=ft.alignment.center_left,
            end=ft.alignment.center_right,
            colors=["#7b2ff7", "#f107a3", "#ff6a00"]
        ),
        leading=ft.IconButton(icon=ft.icons.MENU, on_click=lambda _: (setattr(page, "drawer", drawer), setattr(page.drawer, "open", True), page.update())),
        actions=[ft.IconButton(icon=ft.icons.SEARCH)]
    )

    # Tabs principais com conteúdo centralizado
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Home",
                content=ft.Container(
                    content=ft.Text(f"🏠 Bem-vindo, {nome_usuario}!", size=20),
                    alignment=ft.alignment.center
                )
            ),
            ft.Tab(
                text="Perfil",
                content=ft.Container(
                    content=ft.Text(f"👤 Perfil de {login_user} (ID: {user_id})", size=20),
                    alignment=ft.alignment.center
                )
            ),
            ft.Tab(
                text="Favoritos",
                content=ft.Container(
                    content=ft.Text("⭐ Seus favoritos aqui", size=20),
                    alignment=ft.alignment.center
                )
            ),
        ]
    )
