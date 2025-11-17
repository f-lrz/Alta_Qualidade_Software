"""Testes para a camada de domínio - Entidades."""

import pytest
from clean_architecture.domain.entities import Cliente, Pedido
from clean_architecture.domain.value_objects import ProdutoTipo, CupomTipo
from clean_architecture.domain.exceptions import ClienteInvalidoError


class TestCliente:
    """Testes para a entidade Cliente."""

    def test_criar_cliente_valido(self):
        """Testa criação de cliente com dados válidos."""
        cliente = Cliente(nome="João Silva", email="joao@test.com", cnpj="12345678000100")
        
        assert cliente.nome == "João Silva"
        assert cliente.email == "joao@test.com"
        assert cliente.cnpj == "12345678000100"

    def test_cliente_email_invalido(self):
        """Testa que cliente com email inválido lança exceção."""
        with pytest.raises(ClienteInvalidoError, match="Email inválido"):
            Cliente(nome="João Silva", email="email_invalido", cnpj="12345678000100")

    def test_cliente_sem_nome(self):
        """Testa que cliente sem nome lança exceção."""
        with pytest.raises(ClienteInvalidoError, match="Nome e email são obrigatórios"):
            Cliente(nome="", email="joao@test.com", cnpj="12345678000100")

    def test_cliente_sem_email(self):
        """Testa que cliente sem email lança exceção."""
        with pytest.raises(ClienteInvalidoError, match="Nome e email são obrigatórios"):
            Cliente(nome="João Silva", email="", cnpj="12345678000100")

    def test_cliente_sem_cnpj(self):
        """Testa que cliente sem CNPJ lança exceção."""
        with pytest.raises(ClienteInvalidoError, match="CNPJ é obrigatório"):
            Cliente(nome="João Silva", email="joao@test.com", cnpj="")

    def test_cliente_email_com_arroba_duplo(self):
        """Testa que email com @ duplo é inválido."""
        with pytest.raises(ClienteInvalidoError, match="Email inválido"):
            Cliente(nome="João Silva", email="joao@@test.com", cnpj="12345678000100")

    def test_cliente_email_sem_dominio(self):
        """Testa que email sem domínio é inválido."""
        with pytest.raises(ClienteInvalidoError, match="Email inválido"):
            Cliente(nome="João Silva", email="joao@", cnpj="12345678000100")

    def test_cliente_email_valido_com_subdominios(self):
        """Testa que email com subdomínios é válido."""
        cliente = Cliente(nome="João Silva", email="joao@mail.company.com.br", cnpj="12345678000100")
        assert cliente.email == "joao@mail.company.com.br"


class TestPedido:
    """Testes para a entidade Pedido."""

    def test_criar_pedido_valido(self):
        """Testa criação de pedido válido."""
        pedido = Pedido(
            cliente="Empresa X",
            produto=ProdutoTipo.DIESEL,
            quantidade=100,
            cupom=CupomTipo.MEGA10,
        )
        
        assert pedido.cliente == "Empresa X"
        assert pedido.produto == ProdutoTipo.DIESEL
        assert pedido.quantidade == 100
        assert pedido.cupom == CupomTipo.MEGA10

    def test_pedido_quantidade_zero(self):
        """Testa que pedido com quantidade zero lança exceção."""
        with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
            Pedido(
                cliente="Empresa X",
                produto=ProdutoTipo.DIESEL,
                quantidade=0,
                cupom=None,
            )

    def test_pedido_quantidade_negativa(self):
        """Testa que pedido com quantidade negativa lança exceção."""
        with pytest.raises(ValueError, match="Quantidade deve ser maior que zero"):
            Pedido(
                cliente="Empresa X",
                produto=ProdutoTipo.DIESEL,
                quantidade=-10,
                cupom=None,
            )

    def test_pedido_sem_cupom(self):
        """Testa criação de pedido sem cupom."""
        pedido = Pedido(
            cliente="Empresa X",
            produto=ProdutoTipo.DIESEL,
            quantidade=100,
            cupom=None,
        )
        
        assert pedido.cupom is None
        assert not pedido.tem_cupom

    def test_pedido_tem_cupom(self):
        """Testa propriedade tem_cupom."""
        pedido_com_cupom = Pedido(
            cliente="Empresa X",
            produto=ProdutoTipo.DIESEL,
            quantidade=100,
            cupom=CupomTipo.MEGA10,
        )
        
        pedido_sem_cupom = Pedido(
            cliente="Empresa X",
            produto=ProdutoTipo.DIESEL,
            quantidade=100,
            cupom=None,
        )
        
        assert pedido_com_cupom.tem_cupom
        assert not pedido_sem_cupom.tem_cupom

    def test_pedido_diferentes_produtos(self):
        """Testa criação de pedidos com diferentes produtos."""
        produtos = [
            ProdutoTipo.DIESEL,
            ProdutoTipo.GASOLINA,
            ProdutoTipo.ETANOL,
            ProdutoTipo.LUBRIFICANTE,
        ]
        
        for produto in produtos:
            pedido = Pedido(cliente="Empresa X", produto=produto, quantidade=50, cupom=None)
            assert pedido.produto == produto

    def test_pedido_diferentes_cupons(self):
        """Testa criação de pedidos com diferentes cupons."""
        cupons = [
            CupomTipo.MEGA10,
            CupomTipo.NOVO5,
            CupomTipo.LUB2,
        ]
        
        for cupom in cupons:
            pedido = Pedido(cliente="Empresa X", produto=ProdutoTipo.DIESEL, quantidade=50, cupom=cupom)
            assert pedido.cupom == cupom
