"""Interfaces de repositórios (contratos)."""

from abc import ABC, abstractmethod
from typing import Dict
from ..entities import Cliente


class ClienteRepositoryInterface(ABC):
    """Interface para persistência de clientes."""
    
    @abstractmethod
    def salvar(self, cliente: Cliente) -> None:
        """Salva um cliente."""
        pass
    
    @abstractmethod
    def buscar_por_email(self, email: str) -> Cliente:
        """Busca um cliente por email."""
        pass


class NotificationServiceInterface(ABC):
    """Interface para serviço de notificações."""
    
    @abstractmethod
    def enviar_boas_vindas(self, email: str, nome: str) -> None:
        """Envia email de boas vindas para o cliente."""
        pass
