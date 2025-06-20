import flet as ft

def criar_filtros(aplicar_filtro_callback):
    filtros = {
        "Aberta": ft.Checkbox(label="Aberta", value=True, scale=0.9),
        "Reservada": ft.Checkbox(label="Reservada", value=True, scale=0.9),
        "Fechada": ft.Checkbox(label="Fechada", value=True, scale=0.9),
    }

    for nome, cb in filtros.items():
        def on_change_factory(status):
            def handler(e):
                aplicar_filtro_callback()
            return handler
        cb.on_change = on_change_factory(nome)

    return filtros
