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

    print(f'ID DA MESA {mesa["id"]}')
    
    # Passando o 'callback' corretamente para abrir o diálogo de adicionar pedido
    abrir_dialogo_adicionar_pedido(page, mesa["id"], callback=lambda: reabrir_dialogo_detalles(page, flag))
    
def controler_pagar_item(page, mesa, id_item):
    # Fechar o diálogo de detalhes da mesa
    if page.dialog.open:
        flag = page.dialog  # Armazenar o diálogo atual
        page.dialog.open = False  # Fecha o diálogo de detalhes da mesa
        page.update()  # Atualiza a página para refletir a mudança

    print(f'ID DA MESA {mesa["id"]}/{id_item}')
    
    # Passando o 'callback' corretamente para abrir o diálogo de adicionar pedido
    abrir_dialogo_pagar_item(page, mesa["id"],id_item, callback=lambda: reabrir_dialogo_detalles(page, flag))
   
    mostrar_detalhes(page, mesa)
       
     
def controler_excluir_pedido(page,mesa, id_item):
    # Fechar o diálogo de detalhes da mesa
    if page.dialog.open:
        flag = page.dialog  # Armazenar o diálogo atual
        page.dialog.open = False  # Fecha o diálogo de detalhes da mesa
        page.update()  # Atualiza a página para refletir a mudança

    print(f'ID DA MESA {mesa["id"]}')
    
    # Passando o 'callback' corretamente para abrir o diálogo de adicionar pedido
    abrir_dialogo_excluir_item(page, mesa["id"], callback=lambda: reabrir_dialogo_detalles(page, flag))
    
def reabrir_dialogo_detalles(page, flag):
    # Após o diálogo de adicionar pedido ser fechado, reabre o diálogo de detalhes da mesa
    page.dialog = flag
    page.dialog.open = True  # Reabre o diálogo de detalhes da mesa
    page.update()
     
def mostrar_detalhes(page, mesa):
    """Mostra os detalhes da mesa em um diálogo - versão simplificada"""
    print(f"DEBUG: mostrar_detalhes chamado para mesa: {mesa}")

    # Versão ultra-simplificada para evitar travamentos
    def fechar_dialog(e):
        page.dialog.open = False
        page.update()

    # Criar diálogo simples
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Mesa {mesa.get('nome', 'Desconhecida')}"),
        content=ft.Column([
            ft.Text(f"Cliente: {mesa.get('cliente', 'N/A')}"),
            ft.Text(f"Status: {mesa.get('status', 'N/A')}"),
            ft.Text(f"Total: R$ {mesa.get('total', 0):.2f}")
        ], tight=True),
        actions=[
            ft.TextButton("Fechar", on_click=fechar_dialog)
        ]
    )

    # Mostrar diálogo
    page.dialog = dialog
    page.dialog.open = True
    page.update()
    print("DEBUG: Diálogo simples criado e exibido")



def mostrar_detalhes_completo(page, mesa):
    """Versão completa da função mostrar_detalhes (backup)"""
    print(f"DEBUG: mostrar_detalhes chamado para mesa: {mesa}")
    try:
        linhas, header, total_geral = montar_itens_consumidos(page, mesa, controler_excluir_pedido, controler_pagar_item)
        print(f"DEBUG: itens carregados, total_geral: {total_geral}")
    except Exception as e:
        print(f"DEBUG: Erro ao montar itens: {e}")
        linhas, header, total_geral = [], None, 0

