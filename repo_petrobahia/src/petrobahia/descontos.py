from abc import ABC, abstractmethod
from typing import Optional, Dict
from .domain import ProdutoTipo, CupomTipo

# --- Interface (Strategy) ---

class DescontoStrategy(ABC):
    """Interface para uma estratégia de aplicação de desconto."""
    @abstractmethod
    def aplicar(self, preco: float, pedido: Dict) -> float:
        pass

# --- Estratégias Concretas (OCP) ---

class DescontoNuloStrategy(DescontoStrategy):
    """Padrão Null Object: não aplica desconto."""
    def aplicar(self, preco: float, pedido: Dict) -> float:
        return preco

class DescontoMega10Strategy(DescontoStrategy):
    def aplicar(self, preco: float, pedido: Dict) -> float:
        return preco * 0.90  # 10% de desconto

class DescontoNovo5Strategy(DescontoStrategy):
    def aplicar(self, preco: float, pedido: Dict) -> float:
        return preco * 0.95  # 5% de desconto

class DescontoLub2Strategy(DescontoStrategy):
    def aplicar(self, preco: float, pedido: Dict) -> float:
        # O cupom LUB2 só se aplica se o produto for lubrificante
        if pedido.get("produto") == ProdutoTipo.LUBRIFICANTE:
            return preco - 2.0
        return preco

# --- Contexto / Serviço ---

class DescontoService:
    """Contexto que seleciona a estratégia de desconto correta."""
    def __init__(self):
        self._strategies = {
            CupomTipo.MEGA10: DescontoMega10Strategy(),
            CupomTipo.NOVO5: DescontoNovo5Strategy(),
            CupomTipo.LUB2: DescontoLub2Strategy(),
        }
        self._default_strategy = DescontoNuloStrategy()

    def aplicar(self, preco: float, pedido: Dict, cupom: Optional[CupomTipo]) -> float:
        """Aplica o desconto correto com base no cupom."""
        strategy = self._strategies.get(cupom, self._default_strategy)
        return strategy.aplicar(preco, pedido)