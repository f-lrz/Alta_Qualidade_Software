"""Value Objects do domínio."""

from enum import Enum


class ProdutoTipo(Enum):
    """Tipo de produto disponível."""

    DIESEL = "diesel"
    GASOLINA = "gasolina"
    ETANOL = "etanol"
    LUBRIFICANTE = "lubrificante"


class CupomTipo(Enum):
    """Tipo de cupom de desconto."""

    MEGA10 = "MEGA10"
    NOVO5 = "NOVO5"
    LUB2 = "LUB2"


# Constantes de preço base (podem ser movidas para configuração externa)
BASES_PRECO = {
    "diesel": 3.99,
    "gasolina": 5.19,
    "etanol": 3.59,
    "lubrificante": 25.0,
}
