from abc import ABC, abstractmethod
from .domain import ProdutoTipo

# --- Interface (Strategy) ---

class ArredondamentoStrategy(ABC):
    """Interface para uma estratégia de arredondamento de preço."""
    @abstractmethod
    def arredondar(self, preco: float) -> float:
        pass

# --- Estratégias Concretas (OCP) ---

class ArredondamentoDieselStrategy(ArredondamentoStrategy):
    """Arredonda para 0 casas decimais."""
    def arredondar(self, preco: float) -> float:
        return round(preco, 0)

class ArredondamentoGasolinaStrategy(ArredondamentoStrategy):
    """Arredonda para 2 casas decimais."""
    def arredondar(self, preco: float) -> float:
        return round(preco, 2)

class ArredondamentoPadraoStrategy(ArredondamentoStrategy):
    """Trunca em 2 casas decimais (comportamento legado)."""
    def arredondar(self, preco: float) -> float:
        return float(int(preco * 100) / 100.0)

# --- Contexto / Serviço ---

class ArredondamentoService:
    """Contexto que seleciona a estratégia de arredondamento correta."""
    def __init__(self):
        self._strategies = {
            ProdutoTipo.DIESEL: ArredondamentoDieselStrategy(),
            ProdutoTipo.GASOLINA: ArredondamentoGasolinaStrategy(),
        }
        # Etanol e Lubrificante usam o padrão
        self._default_strategy = ArredondamentoPadraoStrategy()

    def arredondar(self, preco: float, tipo_produto: ProdutoTipo) -> float:
        """Delega o arredondamento para a estratégia correta."""
        strategy = self._strategies.get(tipo_produto, self._default_strategy)
        return strategy.arredondar(preco)