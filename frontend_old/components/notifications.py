import flet as ft
import threading
import time

class NotificationManager:
    """Gerenciador de notificações para feedback visual"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.notifications = []
        self.container = ft.Column(
            controls=[],
            spacing=10,
            alignment=ft.MainAxisAlignment.END,
            horizontal_alignment=ft.CrossAxisAlignment.END
        )
        
    def show_success(self, message: str, duration: int = 3):
        """Mostra notificação de sucesso"""
        self._show_notification(message, ft.Colors.GREEN, ft.Icons.CHECK_CIRCLE, duration)
    
    def show_error(self, message: str, duration: int = 5):
        """Mostra notificação de erro"""
        self._show_notification(message, ft.Colors.RED, ft.Icons.ERROR, duration)
    
    def show_warning(self, message: str, duration: int = 4):
        """Mostra notificação de aviso"""
        self._show_notification(message, ft.Colors.ORANGE, ft.Icons.WARNING, duration)
    
    def show_info(self, message: str, duration: int = 3):
        """Mostra notificação de informação"""
        self._show_notification(message, ft.Colors.BLUE, ft.Icons.INFO, duration)
    
    def _show_notification(self, message: str, color: str, icon: str, duration: int):
        """Mostra uma notificação"""
        notification_id = len(self.notifications)
        
        # Criar o componente da notificação
        notification = ft.Card(
            content=ft.Container(
                content=ft.Row([
                    ft.Icon(icon, color=color, size=20),
                    ft.Text(
                        message,
                        color=ft.Colors.WHITE,
                        size=14,
                        expand=True
                    ),
                    ft.IconButton(
                        icon=ft.Icons.CLOSE,
                        icon_color=ft.Colors.WHITE,
                        icon_size=16,
                        on_click=lambda e: self._remove_notification(notification_id)
                    )
                ], spacing=10),
                padding=15,
                bgcolor=color,
                border_radius=8
            ),
            width=350,
            elevation=6
        )
        
        # Adicionar à lista e ao container
        self.notifications.append(notification)
        self.container.controls.append(notification)
        self.page.update()
        
        # Remover automaticamente após o tempo especificado
        def auto_remove():
            time.sleep(duration)
            self._remove_notification(notification_id)
        
        threading.Thread(target=auto_remove, daemon=True).start()
    
    def _remove_notification(self, notification_id: int):
        """Remove uma notificação"""
        try:
            if notification_id < len(self.notifications):
                notification = self.notifications[notification_id]
                if notification in self.container.controls:
                    self.container.controls.remove(notification)
                    self.page.update()
        except Exception:
            pass
    
    def get_container(self):
        """Retorna o container das notificações"""
        return self.container

def create_loading_indicator(message: str = "Carregando..."):
    """Cria um indicador de carregamento"""
    return ft.Container(
        content=ft.Column([
            ft.ProgressRing(width=40, height=40, stroke_width=4),
            ft.Text(message, size=14, text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
        padding=20,
        alignment=ft.alignment.center,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.BLACK26
        )
    )

def create_confirmation_dialog(title: str, message: str, on_confirm, on_cancel=None):
    """Cria um diálogo de confirmação"""
    return ft.AlertDialog(
        modal=True,
        title=ft.Text(title, weight=ft.FontWeight.BOLD),
        content=ft.Text(message),
        actions=[
            ft.TextButton(
                "Cancelar",
                on_click=lambda e: on_cancel() if on_cancel else None
            ),
            ft.ElevatedButton(
                "Confirmar",
                on_click=lambda e: on_confirm(),
                style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END
    ) 