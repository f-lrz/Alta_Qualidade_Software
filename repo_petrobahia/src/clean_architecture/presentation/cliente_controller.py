"""Controller para operações de cliente."""

from typing import List, Dict
from ..application.use_cases import CadastrarClienteUseCase
from ..application.dto import ClienteInputDTO, ClienteOutputDTO


class ClienteController:
    """Controller responsável por gerenciar operações de cliente."""
    
    def __init__(self, cadastrar_cliente_use_case: CadastrarClienteUseCase):
        self.cadastrar_cliente_use_case = cadastrar_cliente_use_case
    
    def cadastrar_clientes(self, clientes_data: List[Dict]) -> List[ClienteOutputDTO]:
        """Cadastra uma lista de clientes."""
        resultados = []
        
        for cliente_data in clientes_data:
            # Converte dict para DTO
            dto = ClienteInputDTO(
                nome=cliente_data.get("nome", ""),
                email=cliente_data.get("email", ""),
                cnpj=cliente_data.get("cnpj", "")
            )
            
            # Executa o caso de uso
            resultado = self.cadastrar_cliente_use_case.execute(dto)
            resultados.append(resultado)
            
            # Log do resultado
            if resultado.sucesso:
                print(f"✅ Cliente cadastrado: {resultado.nome}")
            else:
                print(f"❌ Erro ao cadastrar cliente: {resultado.mensagem}")
        
        return resultados
