"""Serviços de domínio (Domain Services)."""

from abc import ABC, abstractmethod
from typing import Optional

from ..value_objects import CupomTipo, ProdutoTipo


class CalculoPrecoServiceInterface(ABC):
    """Interface para serviço de cálculo de preço."""

    @abstractmethod
    def calcular(self, produto: ProdutoTipo, quantidade: int) -> float:
        """Calcula o preço base do pedido."""
        pass


class DescontoServiceInterface(ABC):
    """Interface para serviço de aplicação de descontos."""

    @abstractmethod
    def aplicar_desconto(
        self,
        preco: float,
        produto: ProdutoTipo,
        quantidade: int,
        cupom: Optional[CupomTipo],
    ) -> float:
        """Aplica desconto ao preço."""
        pass


class ArredondamentoServiceInterface(ABC):
    """Interface para serviço de arredondamento."""

    @abstractmethod
    def arredondar(self, preco: float, produto: ProdutoTipo) -> float:
        """Arredonda o preço de acordo com as regras do produto."""
        pass
