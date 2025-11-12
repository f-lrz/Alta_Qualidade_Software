"""Entidades do domínio."""

from dataclasses import dataclass
from typing import Optional
import re
from ..exceptions import ClienteInvalidoError
from ..value_objects import ProdutoTipo, CupomTipo


@dataclass
class Cliente:
    """Entidade Cliente com validações de negócio."""
    nome: str
    email: str
    cnpj: str
    
    REG_EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    def __post_init__(self):
        """Valida os dados do cliente após inicialização."""
        self._validar()
    
    def _validar(self):
        """Valida os dados do cliente."""
        if not self.nome or not self.email:
            raise ClienteInvalidoError("Nome e email são obrigatórios.")
        
        if not re.match(self.REG_EMAIL, self.email):
            raise ClienteInvalidoError(f"Email inválido: {self.email}")
        
        if not self.cnpj:
            raise ClienteInvalidoError("CNPJ é obrigatório.")


@dataclass
class Pedido:
    """Entidade Pedido."""
    cliente: str
    produto: ProdutoTipo
    quantidade: int
    cupom: Optional[CupomTipo] = None
    
    def __post_init__(self):
        """Valida os dados do pedido após inicialização."""
        if self.quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
    
    @property
    def tem_cupom(self) -> bool:
        """Verifica se o pedido possui cupom."""
        return self.cupom is not None
