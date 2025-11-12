"""Use Cases da aplicação."""

from .cadastrar_cliente import CadastrarClienteUseCase
from .processar_pedido import ProcessarPedidoUseCase

__all__ = [
    'CadastrarClienteUseCase',
    'ProcessarPedidoUseCase'
]
