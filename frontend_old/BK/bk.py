import flet as ft
from datetime import datetime
import time
import threading
import requests
def painel_view(page: ft.Page, nome_usuario: str = "", tipo_usuario: str = "", user_id: str = "", login_user: str = ""):
    try:
        config = requests.get("http://127.0.0.1:8000/configuracao").json()
        qtd_mesas = config.get("mesas", 0)
    except Exception as e:
        qtd_mesas = 0
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Erro ao carregar configuração: {str(e)}"),
            bgcolor=ft.colors.RED_100
        )
        page.snack_bar.open = True
        page.update()


    mesas = requests.get("http://127.0.0.1:8000/mesas").json()

    hora_text = ft.Text(f"Hora: {datetime.now().strftime('%H:%M:%S')}", size=11)

    def atualizar_relogio():
        while True:
            hora_text.value = f"Hora: {datetime.now().strftime('%H:%M:%S')}"
            page.update()
            time.sleep(1)

    threading.Thread(target=atualizar_relogio, daemon=True).start()

    filtros = {
        "Aberta": ft.Checkbox(label="Aberta", value=True, scale=0.9),
        "Reservada": ft.Checkbox(label="Reservada", value=True, scale=0.9),
        "Fechada": ft.Checkbox(label="Fechada", value=True, scale=0.9),
    }

    mesa_id_input = ft.TextField(label="ID da Mesa", width=200, height=40, text_style=ft.TextStyle(size=10))
    cliente_input = ft.TextField(label="Nome do Cliente", width=250, height=40, text_style=ft.TextStyle(size=10))
    status_dropdown = ft.Dropdown(
        label="Novo Status",
        options=[
            ft.dropdown.Option("Aberta"),
            ft.dropdown.Option("Reservada")
        ],
        width=200,
        height=50,
        value="Aberta"
    )

    def aplicar_filtro():
        nonlocal mesas
        import requests
        mesas = requests.get("http://127.0.0.1:8000/mesas").json()
        status_selecionados = [k for k, cb in filtros.items() if cb.value]
        cards_mesas.controls.clear()
        for mesa in mesas:
            if any(mesa['status'].lower() == s.lower() for s in status_selecionados):
                cards_mesas.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(f"🪑 {mesa['nome']}", size=14, weight=ft.FontWeight.W_600),
                                ft.Text(f"Cliente: {mesa['cliente'] or '---'}", size=10),
                                ft.Text(f"Status: {mesa['status']}", size=10),
                                ft.Text(f"Total: R$ {mesa['total']:.2f}", size=10)
                            ]),
                            padding=10,
                            border_radius=10,
                            bgcolor=ft.colors.BLUE_100,
                            on_click=lambda e, m=mesa: mostrar_detalhes(m)
                        ),
                        width=160
                    )
                )
        page.update()

    for nome, cb in filtros.items():
        def on_change_factory(status):
            def handler(e):
                aplicar_filtro()
            return handler
        cb.on_change = on_change_factory(nome)

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
                

                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao atualizar mesa: {response.status_code} - {erro_detail}"))
                page.update()
            if response.status_code == 200:
                page.snack_bar = ft.SnackBar(ft.Text(f"Mesa {id_mesa} atualizada para {nome} ({status})"))
                page.snack_bar.open = True
                aplicar_filtro()
                return
            else:
                
                page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao atualizar mesa: {response.text}"))
                page.snack_bar.open = True
                page.update()

    mesa_selecionada = ft.Container(visible=False)

    def mostrar_detalhes(mesa):
        print("entrou aqui")
        try:
            print(mesa)
            response = requests.get(f"http://127.0.0.1:8000/consumo/{mesa['id']}")
            response.raise_for_status()
            itens = response.json()
           
        except Exception as err:
            itens = []
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Erro ao buscar itens: {err}"),
                bgcolor=ft.colors.RED_100
            )
            page.snack_bar.open = True
            page.update()
            return

        def pagar_individual(item):
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"💳 Pagamento individual do item '{item['nome']}' no valor de R$ {item['total']:.2f} realizado."),
                bgcolor=ft.colors.GREEN_100
            )
            page.snack_bar.open = True
            page.update()

        total_geral = sum(item["preco"] * item["quantidade"] for item in itens)

        # Cabeçalho da tabela
        header = ft.Row([
        ft.Text("ID", expand=1, weight=ft.FontWeight.BOLD),
        ft.Text("Item", expand=3, weight=ft.FontWeight.BOLD),
        ft.Text("Preço", expand=2, weight=ft.FontWeight.BOLD),
        ft.Text("Qtd", expand=1, weight=ft.FontWeight.BOLD),
        ft.Text("Total", expand=2, weight=ft.FontWeight.BOLD),
        ft.Text("Ações", expand=2, weight=ft.FontWeight.BOLD),
        ], spacing=10)

        # Linhas da tabela com ações
        linhas = []
        for item in itens:
            total_item = item["preco"] * item["quantidade"]
            linhas.append(
                ft.Row([
                    ft.Text(str(item["id"]), expand=1),
                    ft.Text(item["nome"], expand=3),
                    ft.Text(f"R$ {item['preco']:.2f}", expand=2),
                    ft.Text(str(item["quantidade"]), expand=1),
                    ft.Text(f"R$ {total_item:.2f}", expand=2),
                    ft.Row([
                        ft.IconButton(icon=ft.icons.DELETE, icon_color=ft.colors.RED, tooltip="Excluir"),
                        ft.IconButton(
                            icon=ft.icons.ATTACH_MONEY,
                            icon_color=ft.colors.GREEN,
                            tooltip="Pagar item",
                            on_click=lambda e, i=item: pagar_individual(i)
                        )
                    ], expand=2)
                ], spacing=10)
            )

        # Atualiza o painel lateral com tudo
        detalhes = ft.Column([
        ft.Row([
            ft.Text(f"Status: {mesa['status']}", size=10),
            ft.Text(f"Cliente: {mesa['cliente'] or '---'}", size=10),
            ft.Text(f"Cpf/Cnpj: {mesa['cpf_cnpj'] or '---'}", size=10),
            ft.Text(f"Abertura: {datetime.now().strftime('%d/%m/%Y %H:%M')}", size=10),
        ], spacing=20),
        ft.Divider(),
        ft.Text("Itens consumidos:", size=14, weight=ft.FontWeight.W_600),
        header,
        *linhas
        ], scroll=ft.ScrollMode.AUTO)

        page.dialog = ft.AlertDialog(
    modal=True,
    title=ft.Text(f"🪑 {mesa['nome']}"),
    content=ft.Container(content=detalhes, width=700, height=450),
    actions=[
        ft.Row(
            controls=[
                ft.Text(f"Total da Comanda: R$ {total_geral:.2f}", size=16, weight=ft.FontWeight.W_700),
                ft.Row(
                    controls=[
                        ft.ElevatedButton("💰 Finalizar Pagamento", bgcolor=ft.colors.GREEN, color=ft.colors.WHITE, height=40),
                        ft.ElevatedButton("Fechar", on_click=lambda e: setattr(page.dialog, "open", False)),
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    ],
    on_dismiss=lambda e: setattr(page.dialog, "open", False)
)

        page.dialog.open = True
        page.update()

        
    botao_fechar_menu = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.icons.CLOSE,
                icon_color=ft.colors.RED,
                tooltip="Fechar menu",
                on_click=lambda _: (setattr(page.drawer, "open", False), page.update())
            )
        ],
        alignment=ft.MainAxisAlignment.END
    )
    # Controlador do menu lateral estilo "hambúrguer"
    drawer = ft.NavigationDrawer(
    controls=[
        ft.Container(
            width=260,
            padding=0,
            content=ft.Container(
                bgcolor=ft.colors.WHITE,
                padding=10,
                content=ft.Column(
                    controls=[
                        ft.Stack([
                                ft.Container(
                                    content=ft.Image(src="logocliente.png", width=150, height=100, fit=ft.ImageFit.COVER),
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
                        ft.ElevatedButton("📋 Mesas", on_click=lambda _: None, icon=ft.icons.TABLE_RESTAURANT),
                        ft.ElevatedButton("📦 Estoque", on_click=lambda _: None, icon=ft.icons.INVENTORY_2),
                        ft.ElevatedButton("👨‍🍳 Cozinha", on_click=lambda _: None, icon=ft.icons.LUNCH_DINING, height=30),
                        ft.ElevatedButton("📦 Produtos", on_click=lambda _: None, icon=ft.icons.INVENTORY, height=30),
                        ft.Divider(),
                        ft.ElevatedButton("🚪 Sair", on_click=lambda _: page.go("/logout"), icon=ft.icons.LOGOUT)
                    ],
                    spacing=5,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )
    ]
)

    # AppBar com gradiente e botão do menu
    app_bar = ft.AppBar(
        title=ft.Text("Sistema de Controle de Mesas e Pedidos", size=18, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.colors.BLUE_50,
        leading=ft.IconButton(icon=ft.icons.MENU, on_click=lambda _: (setattr(page, "drawer", drawer), setattr(page.drawer, "open", True), page.update())),
        actions=[ft.IconButton(icon=ft.icons.SEARCH)]
    )

    # Tabs principais com conteúdo centralizado
    
    cards_mesas = ft.Row(wrap=True, spacing=10)
    aplicar_filtro()

    filtro_e_abertura = ft.Card(
    elevation=1,
    margin=10,
    content=ft.Container(
        padding=10,
        bgcolor=ft.colors.BLUE_50,
        border_radius=10,
        content=ft.ExpansionTile(
            title=ft.Text("🔍 Filtros e Abertura de Mesas", size=12, weight=ft.FontWeight.W_600),
            initially_expanded=False,
            controls=[
                    ft.ResponsiveRow(
                        columns=12,
                        controls=[
                            # Filtros
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
                            # Abrir Mesa
                            ft.Container(
                                col={"sm": 12, "md": 6},
                                content=ft.Column(
                                    spacing=6,
                                    controls=[
        ft.Text("Abrir mesa por ID", size=11, weight=ft.FontWeight.W_500),

        ft.Container(
            content=ft.Row(
                [mesa_id_input, cliente_input],
                spacing=5,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            margin=ft.margin.only(bottom=10)
        ),

        ft.Row(
            [
                status_dropdown,
                ft.ElevatedButton(
                    "Abrir",
                    icon=ft.icons.ADD,
                    on_click=abrir_mesa,
                    height=35,
                    width=100,
                    style=ft.ButtonStyle(padding=10)
                )
            ],
            spacing=20
        )
    ]

                                )
                            )
                        ]
                    )
                ]
            )
        )
    )

    # Atualiza o conteúdo da página diretamente
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
                    ),
                    ft.Container(
                        content=mesa_selecionada,
                        expand=2,
                        padding=20
                    )
        ],
        appbar=app_bar,
        drawer=drawer,
        scroll=ft.ScrollMode.AUTO
    )
