from typing import Dict, Optional
from .domain import ProdutoTipo, CupomTipo
from .calculos import PrecoCalculadora
from .descontos import DescontoService
from .arredondamento import ArredondamentoService

class PedidoService:
    """Orquestra o processamento de pedidos (SRP)."""
    
    def __init__(
        self,
        calculadora: PrecoCalculadora,
        desconto_svc: DescontoService,
        arredondamento_svc: ArredondamentoService
    ):
        # Injeção de Dependência
        self.calculadora = calculadora
        self.desconto_svc = desconto_svc
        self.arredondamento_svc = arredondamento_svc

    def _parse_pedido(self, pedido_data: Dict) -> (ProdutoTipo, int, Optional[CupomTipo]):
        """Converte os dados do dicionário em tipos de domínio (Enums)."""
        try:
            produto = ProdutoTipo(pedido_data.get("produto"))
        except ValueError:
            raise ValueError(f"Produto desconhecido: {pedido_data.get('produto')}")

        qtd = pedido_data.get("qtd", 0)
        
        cupom_str = pedido_data.get("cupom")
        cupom = None
        if cupom_str:
            try:
                cupom = CupomTipo(cupom_str)
            except ValueError:
                print(f"Aviso: Cupom {cupom_str} desconhecido.")
                
        return produto, qtd, cupom

    def processar_pedido(self, pedido_data: Dict) -> float:
        """
        Processa um pedido orquestrando os serviços de cálculo,
        desconto e arredondamento.
        """
        try:
            produto, qtd, cupom = self._parse_pedido(pedido_data)
        except ValueError as e:
            print(f"Erro ao processar pedido: {e}")
            return 0.0

        # 1. Validação (Gate Clause)
        if qtd <= 0:
            print("qtd zero, retornando 0")
            return 0.0

        # 2. Cálculo (Delega ao Strategy)
        preco = self.calculadora.calcular(produto, qtd)
        if preco < 0:
            print("algo deu errado, preco negativo")
            preco = 0.0

        # 3. Desconto (Delega ao Strategy)
        preco_descontado = self.desconto_svc.aplicar(preco, pedido_data, cupom)

        # 4. Arredondamento (Delega ao Strategy)
        preco_final = self.arredondamento_svc.arredondar(preco_descontado, produto)
        
        print(f"pedido ok: {pedido_data['cliente']} {produto.value} {qtd} => {preco_final}")
        return preco_final