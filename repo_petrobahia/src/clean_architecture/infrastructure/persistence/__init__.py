"""Implementações de repositórios de persistência."""

from typing import Optional
from ...domain.entities import Cliente
from ...domain.repositories import ClienteRepositoryInterface


class ClienteFileRepository(ClienteRepositoryInterface):
    """Implementação de repositório que salva clientes em arquivo."""
    
    def __init__(self, filepath: str = "clientes_clean_arch.txt"):
        self.filepath = filepath
    
    def salvar(self, cliente: Cliente) -> None:
        """Salva o cliente em arquivo."""
        try:
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(f"{cliente.nome}|{cliente.email}|{cliente.cnpj}\n")
        except IOError as e:
            raise Exception(f"Erro ao salvar cliente: {e}")
    
    def buscar_por_email(self, email: str) -> Optional[Cliente]:
        """Busca um cliente por email (implementação simplificada)."""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                for linha in f:
                    dados = linha.strip().split("|")
                    if len(dados) == 3 and dados[1] == email:
                        return Cliente(nome=dados[0], email=dados[1], cnpj=dados[2])
        except FileNotFoundError:
            return None
        return None
