"""Caso de uso: Processar Pedido."""

from typing import Optional

from ...domain.entities import Pedido
from ...domain.exceptions import ProdutoNaoEncontradoError
from ...domain.services import (
    ArredondamentoServiceInterface,
    CalculoPrecoServiceInterface,
    DescontoServiceInterface,
)
from ...domain.value_objects import CupomTipo, ProdutoTipo
from ..dto import PedidoInputDTO, PedidoOutputDTO


class ProcessarPedidoUseCase:
    """
    Caso de uso: Processar um pedido.

    Responsabilidades:
    - Validar dados do pedido
    - Calcular preço
    - Aplicar descontos
    - Arredondar valor final
    """

    def __init__(
        self,
        calculo_preco_service: CalculoPrecoServiceInterface,
        desconto_service: DescontoServiceInterface,
        arredondamento_service: ArredondamentoServiceInterface,
    ):
        self.calculo_preco_service = calculo_preco_service
        self.desconto_service = desconto_service
        self.arredondamento_service = arredondamento_service

    def execute(self, dto: PedidoInputDTO) -> PedidoOutputDTO:
        """Executa o caso de uso de processamento de pedido."""
        try:
            # 1. Converter dados para tipos de domínio
            produto = ProdutoTipo(dto.produto)
            cupom = CupomTipo(dto.cupom) if dto.cupom else None

            # 2. Criar entidade de domínio
            pedido = Pedido(
                cliente=dto.cliente, produto=produto, quantidade=dto.qtd, cupom=cupom
            )

            # 3. Calcular preço base
            preco = self.calculo_preco_service.calcular(
                produto=pedido.produto, quantidade=pedido.quantidade
            )

            # 4. Aplicar desconto
            preco_com_desconto = self.desconto_service.aplicar_desconto(
                preco=preco,
                produto=pedido.produto,
                quantidade=pedido.quantidade,
                cupom=pedido.cupom,
            )

            # 5. Arredondar
            preco_final = self.arredondamento_service.arredondar(
                preco=preco_com_desconto, produto=pedido.produto
            )

            return PedidoOutputDTO(
                cliente=pedido.cliente,
                produto=pedido.produto.value,
                quantidade=pedido.quantidade,
                valor_final=preco_final,
                sucesso=True,
                mensagem="Pedido processado com sucesso",
            )

        except ValueError as e:
            return PedidoOutputDTO(
                cliente=dto.cliente,
                produto=dto.produto,
                quantidade=dto.qtd,
                valor_final=0.0,
                sucesso=False,
                mensagem=f"Erro de validação: {str(e)}",
            )
        except ProdutoNaoEncontradoError as e:
            return PedidoOutputDTO(
                cliente=dto.cliente,
                produto=dto.produto,
                quantidade=dto.qtd,
                valor_final=0.0,
                sucesso=False,
                mensagem=f"Produto não encontrado: {str(e)}",
            )
        except Exception as e:
            return PedidoOutputDTO(
                cliente=dto.cliente,
                produto=dto.produto,
                quantidade=dto.qtd,
                valor_final=0.0,
                sucesso=False,
                mensagem=f"Erro inesperado: {str(e)}",
            )
