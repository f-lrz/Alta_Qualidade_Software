from abc import ABC, abstractmethod
from .domain import ProdutoTipo, BASES_PRECO, ProdutoNaoEncontradoError

# --- Interface (Strategy) ---

class CalculoPrecoStrategy(ABC):
    """Interface para uma estratégia de cálculo de preço."""
    def __init__(self, preco_base: float):
        self.preco_base = preco_base
    
    @abstractmethod
    def calcular(self, qtd: int) -> float:
        """Calcula o preço com base na quantidade."""
        pass

# --- Estratégias Concretas (OCP) ---

class CalculoDieselStrategy(CalculoPrecoStrategy):
    def calcular(self, qtd: int) -> float:
        preco = self.preco_base * qtd
        if qtd > 1000:
            preco *= 0.90  # 10% de desconto
        elif qtd > 500:
            preco *= 0.95  # 5% de desconto
        print(f"calc diesel: {preco}")
        return preco

class CalculoGasolinaStrategy(CalculoPrecoStrategy):
    def calcular(self, qtd: int) -> float:
        preco = self.preco_base * qtd
        if qtd > 200:
            preco -= 100  # Desconto fixo
        print(f"calc gas: {preco}")
        return preco

class CalculoEtanolStrategy(CalculoPrecoStrategy):
    def calcular(self, qtd: int) -> float:
        preco = self.preco_base * qtd
        if qtd > 80:
            preco *= 0.97  # 3% de desconto
        print(f"calc eta: {preco}")
        return preco

class CalculoLubrificanteStrategy(CalculoPrecoStrategy):
    def calcular(self, qtd: int) -> float:
        # Corrige o loop 'for' desnecessário do código legado
        return self.preco_base * qtd

# --- Contexto / Fábrica ---

class PrecoCalculadora:
    """Contexto que seleciona a estratégia de cálculo correta."""
    def __init__(self):
        # Mapeia o Enum ProdutoTipo para a Estratégia concreta
        self._strategies = {
            ProdutoTipo.DIESEL: CalculoDieselStrategy(BASES_PRECO["diesel"]),
            ProdutoTipo.GASOLINA: CalculoGasolinaStrategy(BASES_PRECO["gasolina"]),
            ProdutoTipo.ETANOL: CalculoEtanolStrategy(BASES_PRECO["etanol"]),
            ProdutoTipo.LUBRIFICANTE: CalculoLubrificanteStrategy(BASES_PRECO["lubrificante"]),
        }

    def calcular(self, tipo: ProdutoTipo, qtd: int) -> float:
        """Calcula o preço, delegando para a estratégia correta."""
        if tipo not in self._strategies:
            print(f"tipo desconhecido {tipo}, devolvendo 0")
            raise ProdutoNaoEncontradoError(f"Estratégia de cálculo não encontrada para {tipo}")

        strategy = self._strategies[tipo]
        return strategy.calcular(qtd)