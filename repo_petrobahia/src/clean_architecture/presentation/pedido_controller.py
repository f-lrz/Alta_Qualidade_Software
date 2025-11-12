"""Controller para operações de pedido."""

from typing import List, Dict
from ..application.use_cases import ProcessarPedidoUseCase
from ..application.dto import PedidoInputDTO, PedidoOutputDTO


class PedidoController:
    """Controller responsável por gerenciar operações de pedido."""
    
    def __init__(self, processar_pedido_use_case: ProcessarPedidoUseCase):
        self.processar_pedido_use_case = processar_pedido_use_case
    
    def processar_pedidos(self, pedidos_data: List[Dict]) -> List[PedidoOutputDTO]:
        """Processa uma lista de pedidos."""
        resultados = []
        valores = []
        
        for pedido_data in pedidos_data:
            # Converte dict para DTO
            dto = PedidoInputDTO(
                cliente=pedido_data.get("cliente", ""),
                produto=pedido_data.get("produto", ""),
                qtd=pedido_data.get("qtd", 0),
                cupom=pedido_data.get("cupom")
            )
            
            # Executa o caso de uso
            resultado = self.processar_pedido_use_case.execute(dto)
            resultados.append(resultado)
            
            # Log do resultado
            if resultado.sucesso:
                valores.append(resultado.valor_final)
                print(f"✅ Pedido processado: {resultado.cliente} - "
                      f"{resultado.produto} - Valor: R$ {resultado.valor_final:.2f}")
            else:
                print(f"❌ Erro ao processar pedido: {resultado.mensagem}")
        
        # Exibe total
        if valores:
            print(f"\n💰 TOTAL: R$ {sum(valores):.2f}")
        
        return resultados
