import flet as ft
from datetime import datetime
import requests
from .dialogo_adicionar_pedido import abrir_dialogo_adicionar_pedido  # Certifique-se de importar corretamente a função
from .dialogo_excluir_pedido import abrir_dialogo_excluir_item
from .dialogo_pagar_item import abrir_dialogo_pagar_item
from .consumo_utils import montar_itens_consumidos
linhas= None
header=None
total_geral=None

def controler_adcionar_pedido(page,mesa):
    # Fechar o diálogo de detalhes da mesa
    if page.dialog.open:
        flag = page.dialog  # Armazenar o diálogo atual
        page.dialog.open = False  # Fecha o diálogo de detalhes da mesa
        page.update()  # Atualiza a página para refletir a mudança

    print(f"ID DA MESA {mesa['id']}")
    
    # Passando o 'callback' corretamente para abrir o diálogo de adicionar pedido
    abrir_dialogo_adicionar_pedido(page, mesa["id"], callback=lambda: reabrir_dialogo_detalles(page, flag))
    
def controler_pagar_item(page, mesa, id_item):
    # Fechar o diálogo de detalhes da mesa
    if page.dialog.open:
        flag = page.dialog  # Armazenar o diálogo atual
        page.dialog.open = False  # Fecha o diálogo de detalhes da mesa
        page.update()  # Atualiza a página para refletir a mudança

    print(f"ID DA MESA {mesa['id']}/{id_item}")
    
    # Passando o 'callback' corretamente para abrir o diálogo de adicionar pedido
    abrir_dialogo_pagar_item(page, mesa["id"],id_item, callback=lambda: reabrir_dialogo_detalles(page, flag))
   
    mostrar_detalhes(page,mesa)
       
     
def controler_excluir_pedido(page,mesa, id_item):
    # Fechar o diálogo de detalhes da mesa
    if page.dialog.open:
        flag = page.dialog  # Armazenar o diálogo atual
        page.dialog.open = False  # Fecha o diálogo de detalhes da mesa
        page.update()  # Atualiza a página para refletir a mudança

    print(f"ID DA MESA {mesa['id']}")
    
    # Passando o 'callback' corretamente para abrir o diálogo de adicionar pedido
    abrir_dialogo_excluir_item(page, mesa["id"], callback=lambda: reabrir_dialogo_detalles(page, flag))
    
def reabrir_dialogo_detalles(page, flag):
    # Após o diálogo de adicionar pedido ser fechado, reabre o diálogo de detalhes da mesa
    page.dialog = flag
    page.dialog.open = True  # Reabre o diálogo de detalhes da mesa
    page.update()
     
def mostrar_detalhes(mesa, page):
    
    linhas, header, total_geral = montar_itens_consumidos(page, mesa, controler_excluir_pedido, controler_pagar_item)
    # Criando o diálogo de detalhes da mesa
    
    detalhes = ft.Column([
    ft.Row([
        ft.Text(f"Status: {mesa['status']}", size=10),
        ft.Text(f"Cliente: {mesa['cliente'] or '---'}", size=10),
        ft.Text(f"Cpf/Cnpj: {mesa['cpf_cnpj'] or '---'}", size=10),
        ft.Text(f"Abertura: {datetime.now().strftime('%d/%m/%Y %H:%M')}", size=10),
        ft.IconButton(
            icon=ft.icons.ADD,
            icon_color=ft.Colors.BLUE,
            tooltip="Adicionar Pedido",
            on_click=lambda e: controler_adcionar_pedido(page, mesa['nome'])
        )
            ], spacing=20),
            ft.Divider(),
            ft.Text("Itens consumidos:", size=14, weight=ft.FontWeight.W_600),
            header,
            *linhas
        ], scroll=ft.ScrollMode.AUTO)
    
    mesa_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"\U0001F6D1 {mesa['nome']}"),
        content=ft.Container(content=detalhes, width=700, height=450),
        actions=[
            ft.Row(
                controls=[
                    ft.Text(f"Total da Comanda: R$ {total_geral:.2f}", size=16, weight=ft.FontWeight.W_700),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton("\U0001F4B0 Finalizar Pagamento", bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE, height=40),
                            ft.ElevatedButton("Fechar", on_click=lambda e: setattr(page.dialog, "open", False)),  # Fechar o diálogo de detalhes
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
    page.dialog=mesa_dialog
    page.dialog.open = True
    page.update()
