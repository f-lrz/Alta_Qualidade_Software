"""Casos de uso (Use Cases) da aplicação."""

from typing import Optional

from ...domain.entities import Cliente
from ...domain.exceptions import ClienteInvalidoError
from ...domain.repositories import (
    ClienteRepositoryInterface,
    NotificationServiceInterface,
)
from ..dto import ClienteInputDTO, ClienteOutputDTO


class CadastrarClienteUseCase:
    """
    Caso de uso: Cadastrar um novo cliente.

    Responsabilidades:
    - Validar dados do cliente
    - Persistir cliente
    - Notificar cliente
    """

    def __init__(
        self,
        cliente_repository: ClienteRepositoryInterface,
        notification_service: NotificationServiceInterface,
    ):
        self.cliente_repository = cliente_repository
        self.notification_service = notification_service

    def execute(self, dto: ClienteInputDTO) -> ClienteOutputDTO:
        """Executa o caso de uso de cadastro de cliente."""
        try:
            # 1. Criar entidade de domínio (validação automática)
            cliente = Cliente(nome=dto.nome, email=dto.email, cnpj=dto.cnpj)

            # 2. Persistir
            self.cliente_repository.salvar(cliente)

            # 3. Notificar
            self.notification_service.enviar_boas_vindas(
                email=cliente.email, nome=cliente.nome
            )

            return ClienteOutputDTO(
                nome=cliente.nome,
                email=cliente.email,
                cnpj=cliente.cnpj,
                sucesso=True,
                mensagem="Cliente cadastrado com sucesso",
            )

        except ClienteInvalidoError as e:
            return ClienteOutputDTO(
                nome=dto.nome,
                email=dto.email,
                cnpj=dto.cnpj,
                sucesso=False,
                mensagem=f"Erro de validação: {str(e)}",
            )
        except Exception as e:
            return ClienteOutputDTO(
                nome=dto.nome,
                email=dto.email,
                cnpj=dto.cnpj,
                sucesso=False,
                mensagem=f"Erro inesperado: {str(e)}",
            )
