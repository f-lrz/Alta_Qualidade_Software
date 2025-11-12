"""Serviços de notificação."""

from ...domain.repositories import NotificationServiceInterface


class PrintNotificationService(NotificationServiceInterface):
    """Implementação de notificação via console (para demonstração)."""

    def enviar_boas_vindas(self, email: str, nome: str) -> None:
        """Simula envio de email via print."""
        print(f"📧 Enviando email de boas-vindas para {email} (Cliente: {nome})")


class EmailNotificationService(NotificationServiceInterface):
    """Implementação real de notificação via email (placeholder)."""

    def __init__(self, smtp_config: dict):
        self.smtp_config = smtp_config

    def enviar_boas_vindas(self, email: str, nome: str) -> None:
        """Envia email real (implementação futura)."""
        # Aqui entraria a lógica real de envio de email
        print(f"📧 Email enviado via SMTP para {email} (Cliente: {nome})")
