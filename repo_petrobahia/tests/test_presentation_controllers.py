"""Testes para controllers da camada de apresentação."""

import pytest
from unittest.mock import Mock
from clean_architecture.presentation.cliente_controller import ClienteController
from clean_architecture.presentation.pedido_controller import PedidoController
from clean_architecture.application.dto import (
    ClienteInputDTO,
    ClienteOutputDTO,
    PedidoInputDTO,
    PedidoOutputDTO,
)


class TestClienteController:
    """Testes para o ClienteController."""

    def test_cadastrar_clientes_sucesso(self):
        """Testa cadastro de múltiplos clientes com sucesso."""
        # Arrange
        mock_use_case = Mock()
        controller = ClienteController(cadastrar_cliente_use_case=mock_use_case)
        
        # Simula resposta de sucesso do use case
        mock_use_case.execute.return_value = ClienteOutputDTO(
            nome="João Silva",
            email="joao@test.com",
            cnpj="12345678000100",
            sucesso=True,
            mensagem="Cliente cadastrado com sucesso",
        )
        
        clientes_data = [
            {"nome": "João Silva", "email": "joao@test.com", "cnpj": "12345678000100"},
            {"nome": "Maria Silva", "email": "maria@test.com", "cnpj": "98765432000100"},
        ]

        # Act
        resultados = controller.cadastrar_clientes(clientes_data)

        # Assert
        assert len(resultados) == 2
        assert all(r.sucesso for r in resultados)
        assert mock_use_case.execute.call_count == 2

    def test_cadastrar_clientes_com_falha(self, capsys):
        """Testa cadastro com falha em alguns clientes."""
        # Arrange
        mock_use_case = Mock()
        controller = ClienteController(cadastrar_cliente_use_case=mock_use_case)
        
        # Simula respostas diferentes
        mock_use_case.execute.side_effect = [
            ClienteOutputDTO(
                nome="João Silva",
                email="joao@test.com",
                cnpj="12345678000100",
                sucesso=True,
                mensagem="Cliente cadastrado com sucesso",
            ),
            ClienteOutputDTO(
                nome="Maria Silva",
                email="email_invalido",
                cnpj="98765432000100",
                sucesso=False,
                mensagem="Email inválido",
            ),
        ]
        
        clientes_data = [
            {"nome": "João Silva", "email": "joao@test.com", "cnpj": "12345678000100"},
            {"nome": "Maria Silva", "email": "email_invalido", "cnpj": "98765432000100"},
        ]

        # Act
        resultados = controller.cadastrar_clientes(clientes_data)

        # Assert
        assert len(resultados) == 2
        assert resultados[0].sucesso is True
        assert resultados[1].sucesso is False
        
        # Verifica os prints
        captured = capsys.readouterr()
        assert "✅ Cliente cadastrado: João Silva" in captured.out
        assert "❌ Erro ao cadastrar cliente: Email inválido" in captured.out

    def test_cadastrar_clientes_lista_vazia(self):
        """Testa cadastro com lista vazia."""
        # Arrange
        mock_use_case = Mock()
        controller = ClienteController(cadastrar_cliente_use_case=mock_use_case)

        # Act
        resultados = controller.cadastrar_clientes([])

        # Assert
        assert len(resultados) == 0
        mock_use_case.execute.assert_not_called()

    def test_cadastrar_clientes_dados_faltando(self):
        """Testa cadastro com dados faltando."""
        # Arrange
        mock_use_case = Mock()
        controller = ClienteController(cadastrar_cliente_use_case=mock_use_case)
        
        mock_use_case.execute.return_value = ClienteOutputDTO(
            nome="",
            email="",
            cnpj="",
            sucesso=False,
            mensagem="Nome e email são obrigatórios",
        )
        
        # Dados incompletos
        clientes_data = [{"nome": ""}]  # Faltam email e cnpj

        # Act
        resultados = controller.cadastrar_clientes(clientes_data)

        # Assert
        assert len(resultados) == 1
        assert resultados[0].sucesso is False


class TestPedidoController:
    """Testes para o PedidoController."""

    def test_processar_pedidos_sucesso(self, capsys):
        """Testa processamento de múltiplos pedidos com sucesso."""
        # Arrange
        mock_use_case = Mock()
        controller = PedidoController(processar_pedido_use_case=mock_use_case)
        
        # Simula respostas de sucesso
        mock_use_case.execute.side_effect = [
            PedidoOutputDTO(
                cliente="Empresa X",
                produto="diesel",
                quantidade=100,
                valor_final=359.0,
                sucesso=True,
                mensagem="Pedido processado com sucesso",
            ),
            PedidoOutputDTO(
                cliente="Empresa Y",
                produto="gasolina",
                quantidade=200,
                valor_final=1038.0,
                sucesso=True,
                mensagem="Pedido processado com sucesso",
            ),
        ]
        
        pedidos_data = [
            {"cliente": "Empresa X", "produto": "diesel", "qtd": 100, "cupom": "MEGA10"},
            {"cliente": "Empresa Y", "produto": "gasolina", "qtd": 200, "cupom": None},
        ]

        # Act
        resultados = controller.processar_pedidos(pedidos_data)

        # Assert
        assert len(resultados) == 2
        assert all(r.sucesso for r in resultados)
        assert mock_use_case.execute.call_count == 2
        
        # Verifica cálculo do total
        captured = capsys.readouterr()
        assert "TOTAL: R$ 1397.00" in captured.out

    def test_processar_pedidos_com_falha(self, capsys):
        """Testa processamento com falha em alguns pedidos."""
        # Arrange
        mock_use_case = Mock()
        controller = PedidoController(processar_pedido_use_case=mock_use_case)
        
        # Simula respostas diferentes
        mock_use_case.execute.side_effect = [
            PedidoOutputDTO(
                cliente="Empresa X",
                produto="diesel",
                quantidade=100,
                valor_final=359.0,
                sucesso=True,
                mensagem="Pedido processado com sucesso",
            ),
            PedidoOutputDTO(
                cliente="Empresa Y",
                produto="produto_invalido",
                quantidade=100,
                valor_final=0.0,
                sucesso=False,
                mensagem="Produto não encontrado",
            ),
        ]
        
        pedidos_data = [
            {"cliente": "Empresa X", "produto": "diesel", "qtd": 100, "cupom": None},
            {"cliente": "Empresa Y", "produto": "produto_invalido", "qtd": 100, "cupom": None},
        ]

        # Act
        resultados = controller.processar_pedidos(pedidos_data)

        # Assert
        assert len(resultados) == 2
        assert resultados[0].sucesso is True
        assert resultados[1].sucesso is False
        
        # Verifica os prints
        captured = capsys.readouterr()
        assert "✅ Pedido processado: Empresa X" in captured.out
        assert "❌ Erro ao processar pedido" in captured.out
        assert "TOTAL: R$ 359.00" in captured.out

    def test_processar_pedidos_lista_vazia(self, capsys):
        """Testa processamento com lista vazia."""
        # Arrange
        mock_use_case = Mock()
        controller = PedidoController(processar_pedido_use_case=mock_use_case)

        # Act
        resultados = controller.processar_pedidos([])

        # Assert
        assert len(resultados) == 0
        mock_use_case.execute.assert_not_called()
        
        # Não deve exibir total se não há pedidos
        captured = capsys.readouterr()
        assert "TOTAL" not in captured.out

    def test_processar_pedidos_todos_com_falha(self, capsys):
        """Testa processamento onde todos falham."""
        # Arrange
        mock_use_case = Mock()
        controller = PedidoController(processar_pedido_use_case=mock_use_case)
        
        # Todos falham
        mock_use_case.execute.return_value = PedidoOutputDTO(
            cliente="Empresa X",
            produto="invalido",
            quantidade=0,
            valor_final=0.0,
            sucesso=False,
            mensagem="Erro",
        )
        
        pedidos_data = [
            {"cliente": "Empresa X", "produto": "invalido", "qtd": 0, "cupom": None},
        ]

        # Act
        resultados = controller.processar_pedidos(pedidos_data)

        # Assert
        assert len(resultados) == 1
        assert resultados[0].sucesso is False
        
        # Não deve exibir total se todos falharam
        captured = capsys.readouterr()
        assert "TOTAL" not in captured.out

    def test_processar_pedidos_dados_faltando(self):
        """Testa processamento com dados faltando."""
        # Arrange
        mock_use_case = Mock()
        controller = PedidoController(processar_pedido_use_case=mock_use_case)
        
        mock_use_case.execute.return_value = PedidoOutputDTO(
            cliente="",
            produto="",
            quantidade=0,
            valor_final=0.0,
            sucesso=False,
            mensagem="Dados inválidos",
        )
        
        # Dados incompletos
        pedidos_data = [{"cliente": ""}]  # Faltam dados

        # Act
        resultados = controller.processar_pedidos(pedidos_data)

        # Assert
        assert len(resultados) == 1
        assert resultados[0].sucesso is False
