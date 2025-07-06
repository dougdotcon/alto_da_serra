import flet as ft
import requests
from datetime import datetime

def abrir_finalizacao_pagamento(mesa, page, total_geral):
    """Abre o diálogo de finalização de pagamento"""
    
    # Estados do pagamento
    forma_pagamento = ft.Ref[ft.Dropdown]()
    valor_pago = ft.Ref[ft.TextField]()
    desconto = ft.Ref[ft.TextField]()
    observacoes = ft.Ref[ft.TextField]()
    
    # Cálculos
    total_com_desconto = ft.Ref[ft.Text]()
    troco = ft.Ref[ft.Text]()
    
    def calcular_valores():
        """Calcula valores com desconto e troco"""
        try:
            desc = float(desconto.current.value or "0")
            pago = float(valor_pago.current.value or "0")
            
            total_final = total_geral - desc
            troco_valor = pago - total_final if pago > total_final else 0
            
            total_com_desconto.current.value = f"R$ {total_final:.2f}"
            total_com_desconto.current.color = ft.Colors.GREEN_700 if total_final >= 0 else ft.Colors.RED
            
            troco.current.value = f"R$ {troco_valor:.2f}"
            troco.current.color = ft.Colors.BLUE_700 if troco_valor > 0 else ft.Colors.GREY
            
            page.update()
        except ValueError:
            pass
    
    def finalizar_pagamento():
        """Finaliza o pagamento e fecha a mesa"""
        try:
            if not forma_pagamento.current.value:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Selecione uma forma de pagamento!"), 
                    bgcolor=ft.Colors.RED
                )
                page.snack_bar.open = True
                page.update()
                return
            
            valor_pago_final = float(valor_pago.current.value or "0")
            desconto_final = float(desconto.current.value or "0")
            total_final = total_geral - desconto_final
            
            if valor_pago_final < total_final:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Valor pago é menor que o total!"), 
                    bgcolor=ft.Colors.RED
                )
                page.snack_bar.open = True
                page.update()
                return
            
            # Fechar mesa usando a rota específica
            response = requests.post("http://127.0.0.1:8000/fechar_mesa", json={
                "mesa_id": mesa['id'],
                "forma_pagamento": forma_pagamento.current.value,
                "valor_pago": valor_pago_final,
                "desconto": desconto_final,
                "observacoes": observacoes.current.value or ""
            })
            
            if response.status_code == 200:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Pagamento finalizado com sucesso!"), 
                    bgcolor=ft.Colors.GREEN
                )
                page.snack_bar.open = True
                page.dialog.open = False
                page.update()
                
                # Mostrar resumo do pagamento
                mostrar_comprovante(mesa, total_geral, desconto_final, valor_pago_final, 
                                  forma_pagamento.current.value, observacoes.current.value, page)
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Erro ao finalizar pagamento!"), 
                    bgcolor=ft.Colors.RED
                )
                page.snack_bar.open = True
                page.update()
                
        except ValueError:
            page.snack_bar = ft.SnackBar(
                ft.Text("Valores inválidos!"), 
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Erro: {str(e)}"), 
                bgcolor=ft.Colors.RED
            )
            page.snack_bar.open = True
            page.update()
    
    # Interface do diálogo
    conteudo = ft.Column([
        # Resumo da conta
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Resumo da Conta", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Row([
                        ft.Text("Subtotal:", size=14),
                        ft.Text(f"R$ {total_geral:.2f}", size=14, weight=ft.FontWeight.BOLD)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row([
                        ft.Text("Desconto:", size=14),
                        ft.TextField(
                            ref=desconto,
                            label="R$ 0,00",
                            width=100,
                            height=40,
                            keyboard_type=ft.KeyboardType.NUMBER,
                            on_change=lambda e: calcular_valores()
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(),
                    ft.Row([
                        ft.Text("Total Final:", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            ref=total_com_desconto,
                            value=f"R$ {total_geral:.2f}",
                            size=16, 
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_700
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=10),
                padding=15
            )
        ),
        
        # Forma de pagamento
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Forma de Pagamento", size=16, weight=ft.FontWeight.BOLD),
                    ft.Dropdown(
                        ref=forma_pagamento,
                        label="Selecione a forma de pagamento",
                        options=[
                            ft.dropdown.Option("Dinheiro"),
                            ft.dropdown.Option("Cartão de Débito"),
                            ft.dropdown.Option("Cartão de Crédito"),
                            ft.dropdown.Option("PIX"),
                            ft.dropdown.Option("Misto")
                        ],
                        width=300
                    )
                ], spacing=10),
                padding=15
            )
        ),
        
        # Valor pago e troco
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Pagamento", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        ft.TextField(
                            ref=valor_pago,
                            label="Valor Pago",
                            width=150,
                            keyboard_type=ft.KeyboardType.NUMBER,
                            on_change=lambda e: calcular_valores()
                        ),
                        ft.Column([
                            ft.Text("Troco:", size=12),
                            ft.Text(
                                ref=troco,
                                value="R$ 0,00",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700
                            )
                        ])
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=10),
                padding=15
            )
        ),
        
        # Observações
        ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Observações", size=16, weight=ft.FontWeight.BOLD),
                    ft.TextField(
                        ref=observacoes,
                        label="Observações do pagamento (opcional)",
                        multiline=True,
                        max_lines=3,
                        width=400
                    )
                ], spacing=10),
                padding=15
            )
        )
    ], spacing=15, scroll=ft.ScrollMode.AUTO)
    
    # Diálogo principal
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon(ft.Icons.PAYMENT, color=ft.Colors.GREEN, size=24),
            ft.Text(f"Finalizar Pagamento - {mesa['nome']}", size=18, weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Container(
            content=conteudo,
            width=500,
            height=600
        ),
        actions=[
            ft.Row([
                ft.ElevatedButton(
                    "Cancelar",
                    icon=ft.Icons.CANCEL,
                    bgcolor=ft.Colors.GREY,
                    color=ft.Colors.WHITE,
                    on_click=lambda e: setattr(page.dialog, "open", False)
                ),
                ft.ElevatedButton(
                    "Finalizar Pagamento",
                    icon=ft.Icons.CHECK,
                    bgcolor=ft.Colors.GREEN,
                    color=ft.Colors.WHITE,
                    on_click=lambda e: finalizar_pagamento()
                )
            ], alignment=ft.MainAxisAlignment.END, spacing=10)
        ]
    )
    
    page.dialog = dialog
    page.dialog.open = True
    page.update()

def mostrar_comprovante(mesa, total_original, desconto, valor_pago, forma_pagamento, observacoes, page):
    """Mostra o comprovante do pagamento"""
    
    total_final = total_original - desconto
    troco = valor_pago - total_final if valor_pago > total_final else 0
    
    comprovante = ft.Column([
        ft.Container(
            content=ft.Column([
                ft.Text("COMPROVANTE DE PAGAMENTO", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Divider(),
                ft.Text(f"Mesa: {mesa['nome']}", size=14),
                ft.Text(f"Cliente: {mesa['cliente'] or 'Não informado'}", size=14),
                ft.Text(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", size=14),
                ft.Divider(),
                ft.Row([
                    ft.Text("Subtotal:", size=14),
                    ft.Text(f"R$ {total_original:.2f}", size=14)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Desconto:", size=14),
                    ft.Text(f"R$ {desconto:.2f}", size=14)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Total:", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(f"R$ {total_final:.2f}", size=16, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Row([
                    ft.Text("Forma de Pagamento:", size=14),
                    ft.Text(forma_pagamento, size=14, weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Valor Pago:", size=14),
                    ft.Text(f"R$ {valor_pago:.2f}", size=14)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([
                    ft.Text("Troco:", size=14),
                    ft.Text(f"R$ {troco:.2f}", size=14, color=ft.Colors.BLUE_700)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ] + ([ft.Divider(), ft.Text(f"Obs: {observacoes}", size=12)] if observacoes else []),
            spacing=8),
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8
        )
    ])
    
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Icon(ft.Icons.RECEIPT, color=ft.Colors.GREEN, size=24),
            ft.Text("Pagamento Realizado", size=18, weight=ft.FontWeight.BOLD)
        ], spacing=10),
        content=ft.Container(
            content=comprovante,
            width=400,
            height=500
        ),
        actions=[
            ft.Row([
                ft.ElevatedButton(
                    "Imprimir",
                    icon=ft.Icons.PRINT,
                    bgcolor=ft.Colors.BLUE,
                    color=ft.Colors.WHITE,
                    on_click=lambda e: page.snack_bar.update(
                        ft.SnackBar(ft.Text("Funcionalidade de impressão em desenvolvimento"))
                    )
                ),
                ft.ElevatedButton(
                    "Fechar",
                    icon=ft.Icons.CLOSE,
                    bgcolor=ft.Colors.GREY,
                    color=ft.Colors.WHITE,
                    on_click=lambda e: setattr(page.dialog, "open", False)
                )
            ], alignment=ft.MainAxisAlignment.END, spacing=10)
        ]
    )
    
    page.dialog = dialog
    page.dialog.open = True
    page.update() 