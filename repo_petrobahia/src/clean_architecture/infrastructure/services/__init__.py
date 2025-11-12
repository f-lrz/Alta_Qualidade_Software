"""Implementações dos serviços de domínio."""

from typing import Optional

from ...domain.exceptions import ProdutoNaoEncontradoError
from ...domain.services import (
    ArredondamentoServiceInterface,
    CalculoPrecoServiceInterface,
    DescontoServiceInterface,
)
from ...domain.value_objects import BASES_PRECO, CupomTipo, ProdutoTipo

# ===== SERVIÇO DE CÁLCULO DE PREÇO =====


class CalculoPrecoService(CalculoPrecoServiceInterface):
    """Implementação do serviço de cálculo de preço usando Strategy Pattern."""

    def calcular(self, produto: ProdutoTipo, quantidade: int) -> float:
        """Calcula o preço base com descontos por volume."""

        if produto == ProdutoTipo.DIESEL:
            preco = BASES_PRECO["diesel"] * quantidade
            if quantidade > 1000:
                preco *= 0.90  # 10% desconto
            elif quantidade > 500:
                preco *= 0.95  # 5% desconto
            return preco

        elif produto == ProdutoTipo.GASOLINA:
            preco = BASES_PRECO["gasolina"] * quantidade
            if quantidade > 200:
                preco -= 100  # Desconto fixo
            return preco

        elif produto == ProdutoTipo.ETANOL:
            preco = BASES_PRECO["etanol"] * quantidade
            if quantidade > 80:
                preco *= 0.97  # 3% desconto
            return preco

        elif produto == ProdutoTipo.LUBRIFICANTE:
            return BASES_PRECO["lubrificante"] * quantidade

        else:
            raise ProdutoNaoEncontradoError(f"Produto não suportado: {produto}")


# ===== SERVIÇO DE DESCONTO =====


class DescontoService(DescontoServiceInterface):
    """Implementação do serviço de aplicação de descontos por cupom."""

    def aplicar_desconto(
        self,
        preco: float,
        produto: ProdutoTipo,
        quantidade: int,
        cupom: Optional[CupomTipo],
    ) -> float:
        """Aplica desconto baseado no cupom."""

        if cupom is None:
            return preco

        if cupom == CupomTipo.MEGA10:
            return preco * 0.90  # 10% desconto

        elif cupom == CupomTipo.NOVO5:
            return preco * 0.95  # 5% desconto

        elif cupom == CupomTipo.LUB2:
            # Cupom LUB2 só funciona para lubrificante
            if produto == ProdutoTipo.LUBRIFICANTE:
                return preco - 2.0
            return preco

        return preco


# ===== SERVIÇO DE ARREDONDAMENTO =====


class ArredondamentoService(ArredondamentoServiceInterface):
    """Implementação do serviço de arredondamento por tipo de produto."""

    def arredondar(self, preco: float, produto: ProdutoTipo) -> float:
        """Arredonda o preço de acordo com as regras do produto."""

        if produto == ProdutoTipo.DIESEL:
            # Diesel: sem casas decimais
            return round(preco, 0)

        elif produto == ProdutoTipo.GASOLINA:
            # Gasolina: 2 casas decimais
            return round(preco, 2)

        else:
            # Etanol e Lubrificante: trunca em 2 casas (comportamento legado)
            return float(int(preco * 100) / 100.0)
