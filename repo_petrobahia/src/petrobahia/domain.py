from enum import Enum, auto

# --- Constantes de Preço Base ---
# Movido do 'preco_calculadora' original
BASES_PRECO = {
    "diesel": 3.99,
    "gasolina": 5.19,
    "etanol": 3.59,
    "lubrificante": 25.0,
}

# --- Enumerações para Tipos (Evita Magic Strings) ---

class ProdutoTipo(Enum):
    DIESEL = "diesel"
    GASOLINA = "gasolina"
    ETANOL = "etanol"
    LUBRIFICANTE = "lubrificante"

class CupomTipo(Enum):
    MEGA10 = "MEGA10"
    NOVO5 = "NOVO5"
    LUB2 = "LUB2"

# --- Exceções Customizadas ---

class ValidacaoError(Exception):
    """Erro para falhas na validação de dados (ex: cliente)."""
    pass

class ProdutoNaoEncontradoError(Exception):
    """Erro quando um tipo de produto desconhecido é solicitado."""
    pass