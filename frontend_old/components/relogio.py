import flet as ft
from datetime import datetime
import threading
import time

def construir_relogio(page):
    hora_text = ft.Text(f"Hora: {datetime.now().strftime('%H:%M:%S')}", size=11)

    def atualizar():
        while True:
            hora_text.value = f"Hora: {datetime.now().strftime('%H:%M:%S')}",
            page.update()
            time.sleep(1)

    threading.Thread(target=atualizar, daemon=True).start()
    return hora_text
