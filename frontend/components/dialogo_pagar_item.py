import flet as ft
import requests

def abrir_dialogo_pagar_item(page, mesa_id,id_item, callback):
    # Busca dados do item
    print("chegou aqui")
    try:
        response = requests.get(f"http://127.0.0.1:8000/consumo/{mesa_id}")
        item = next((i for i in response.json() if i['id'] == id_item), None)
        if not item:
            raise Exception("Item não encontrado.")
    except Exception as e:
        page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {str(e)}"))
        page.snack_bar.open = True
        page.update()
        return

    # Campo para digitar a quantidade a abater
    quantidade_input = ft.TextField(
        label="Quantidade a abater",
        width=150,
        height=40,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    novo_total_text = ft.Text("Novo Total: R$ 0.00", size=14, weight=ft.FontWeight.BOLD)

    # Calcula novo total
    def calcular_novo_total(e):
        try:
            quantidade = int(quantidade_input.value)
            if quantidade > item['quantidade']:
                novo_total_text.value = "Erro: Quantidade maior que a atual."
            else:
                nova_quantidade = item['quantidade'] - quantidade
                novo_total = nova_quantidade * item['preco']
                novo_total_text.value = f"Novo Total: R$ {novo_total:.2f}"
        except:
            novo_total_text.value = "Erro na quantidade."
        page.update()

    # Cancelar
    def cancelar(e):
        page.dialog.open = False
        page.update()
        callback()

    # Confirmar
    def confirmar(e):
        try:
            quantidade = int(quantidade_input.value)
            res = requests.post("http://127.0.0.1:8000/abater_consumo", json={
                "consumo_id": id_item,
                "mesa_id": mesa_id,
                "quantidade": quantidade
            })
            if res.status_code == 200:
                page.snack_bar = ft.SnackBar(ft.Text("Item atualizado com sucesso!"))
            else:
                raise Exception(res.json()["detail"])
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {str(ex)}"))
        finally:
            page.snack_bar.open = True
            page.dialog.open = False
            page.update()
            callback()

    # Layout
    conteudo = ft.Column([
        ft.Text(f"Produto: {item['nome']} (R$ {item['preco']:.2f})", size=14),
        ft.Text(f"Quantidade atual: {item['quantidade']}", size=14),
        ft.Text(f"Total atual: R$ {item['total']:.2f}", size=14),
        quantidade_input,
        novo_total_text
    ], spacing=10)

    container = ft.Container(content=conteudo, width=400, height=300, padding=20)

    dialogo_pagar = ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Pagar Item - Mesa {mesa_id}"),
        content=container,
        actions=[
            ft.TextButton("Cancelar", on_click=cancelar),
            ft.TextButton("Confirmar", on_click=confirmar)
        ],
        on_dismiss=lambda e: page.overlay.remove(dialogo_pagar)
    )

    quantidade_input.on_change = calcular_novo_total

    page.dialog = dialogo_pagar
    page.dialog.open = True
    page.update()
