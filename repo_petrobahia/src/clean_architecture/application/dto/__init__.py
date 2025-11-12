"""Data Transfer Objects (DTOs) para comunicação entre camadas."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ClienteInputDTO:
    """DTO para entrada de dados de cliente."""

    nome: str
    email: str
    cnpj: str


@dataclass
class ClienteOutputDTO:
    """DTO para saída de dados de cliente."""

    nome: str
    email: str
    cnpj: str
    sucesso: bool
    mensagem: Optional[str] = None


@dataclass
class PedidoInputDTO:
    """DTO para entrada de dados de pedido."""

    cliente: str
    produto: str
    qtd: int
    cupom: Optional[str] = None


@dataclass
class PedidoOutputDTO:
    """DTO para saída de dados de pedido."""

    cliente: str
    produto: str
    quantidade: int
    valor_final: float
    sucesso: bool
    mensagem: Optional[str] = None
