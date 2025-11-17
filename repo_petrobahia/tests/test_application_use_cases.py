"""Testes para casos de uso - Application Layer."""

import pytest
from unittest.mock import Mock, call
from clean_architecture.application.use_cases import CadastrarClienteUseCase, ProcessarPedidoUseCase
from clean_architecture.application.dto import (
    ClienteInputDTO,
    ClienteOutputDTO,
    PedidoInputDTO,
    PedidoOutputDTO,
)
from clean_architecture.domain.entities import Cliente, Pedido
from clean_architecture.domain.value_objects import ProdutoTipo, CupomTipo
from clean_architecture.domain.exceptions import ClienteInvalidoError


class TestCadastrarClienteUseCase:
    """Testes para o caso de uso CadastrarClienteUseCase."""

    def test_cadastrar_cliente_sucesso(
        self, mock_cliente_repository, mock_notification_service
    ):
        """Testa cadastro de cliente com sucesso."""
        # Arrange
        use_case = CadastrarClienteUseCase(
            cliente_repository=mock_cliente_repository,
            notification_service=mock_notification_service,
        )
        
        dto = ClienteInputDTO(
            nome="João Silva",
            email="joao@test.com",
            cnpj="12345678000100",
        )

        # Act
        resultado = use_case.execute(dto)

        # Assert
        assert resultado.sucesso is True
        assert resultado.nome == "João Silva"
        assert resultado.email == "joao@test.com"
        assert resultado.mensagem == "Cliente cadastrado com sucesso"
        
        # Verifica que o repositório foi chamado
        mock_cliente_repository.salvar.assert_called_once()
        
        # Verifica que a notificação foi enviada
        mock_notification_service.enviar_boas_vindas.assert_called_once_with(
            email="joao@test.com", nome="João Silva"
        )

    def test_cadastrar_cliente_email_invalido(
        self, mock_cliente_repository, mock_notification_service
    ):
        """Testa cadastro de cliente com email inválido."""
        # Arrange
        use_case = CadastrarClienteUseCase(
            cliente_repository=mock_cliente_repository,
            notification_service=mock_notification_service,
        )
        
        dto = ClienteInputDTO(
            nome="João Silva",
            email="email_invalido",
            cnpj="12345678000100",
        )

        # Act
        resultado = use_case.execute(dto)

        # Assert
        assert resultado.sucesso is False
        assert "Email inválido" in resultado.mensagem
        
        # Verifica que o repositório NÃO foi chamado
        mock_cliente_repository.salvar.assert_not_called()
        
        # Verifica que a notificação NÃO foi enviada
        mock_notification_service.enviar_boas_vindas.assert_not_called()

    def test_cadastrar_cliente_sem_nome(
        self, mock_cliente_repository, mock_notification_service
    ):
        """Testa cadastro de cliente sem nome."""
        # Arrange
        use_case = CadastrarClienteUseCase(
            cliente_repository=mock_cliente_repository,
            notification_service=mock_notification_service,
        )
        
        dto = ClienteInputDTO(
            nome="",
            email="joao@test.com",
            cnpj="12345678000100",
        )

        # Act
        resultado = use_case.execute(dto)

        # Assert
        assert resultado.sucesso is False
        assert "obrigatórios" in resultado.mensagem
        mock_cliente_repository.salvar.assert_not_called()

    def test_cadastrar_cliente_erro_repositorio(
        self, mock_cliente_repository, mock_notification_service
    ):
        """Testa comportamento quando repositório lança exceção."""
        # Arrange
        use_case = CadastrarClienteUseCase(
            cliente_repository=mock_cliente_repository,
            notification_service=mock_notification_service,
        )
        
        dto = ClienteInputDTO(
            nome="João Silva",
            email="joao@test.com",
            cnpj="12345678000100",
        )
        
        # Simula erro no repositório
        mock_cliente_repository.salvar.side_effect = Exception("Erro de conexão")

        # Act
        resultado = use_case.execute(dto)

        # Assert
        assert resultado.sucesso is False
        assert "Erro inesperado" in resultado.mensagem
        assert "Erro de conexão" in resultado.mensagem


class TestProcessarPedidoUseCase:
    """Testes para o caso de uso ProcessarPedidoUseCase."""

    def test_processar_pedido_sucesso(
        self,
        mock_calculo_preco_service,
        mock_desconto_service,
        mock_arredondamento_service,
    ):
        """Testa processamento de pedido com sucesso."""
        # Arrange
        use_case = ProcessarPedidoUseCase(
            calculo_preco_service=mock_calculo_preco_service,
            desconto_service=mock_desconto_service,
            arredondamento_service=mock_arredondamento_service,
        )
        
        dto = PedidoInputDTO(
            cliente="Empresa X",
            produto="diesel",
            qtd=100,
            cupom="MEGA10",
        )
        
        # Configura mocks
        mock_calculo_preco_service.calcular.return_value = 399.0
        mock_desconto_service.aplicar_desconto.return_value = 359.1
        mock_arredondamento_service.arredondar.return_value = 359.0

        # Act
        resultado = use_case.execute(dto)

        # Assert
        assert resultado.sucesso is True
        assert resultado.cliente == "Empresa X"
        assert resultado.produto == "diesel"
        assert resultado.quantidade == 100
        assert resultado.valor_final == 359.0
        assert "sucesso" in resultado.mensagem.lower()
        
        # Verifica chamadas aos serviços
        mock_calculo_preco_service.calcular.assert_called_once()
        mock_desconto_service.aplicar_desconto.assert_called_once()
        mock_arredondamento_service.arredondar.assert_called_once()

    def test_processar_pedido_sem_cupom(
        self,
        mock_calculo_preco_service,
        mock_desconto_service,
        mock_arredondamento_service,
    ):
        """Testa processamento de pedido sem cupom."""
        # Arrange
        use_case = ProcessarPedidoUseCase(
            calculo_preco_service=mock_calculo_preco_service,
            desconto_service=mock_desconto_service,
            arredondamento_service=mock_arredondamento_service,
        )
        
        dto = PedidoInputDTO(
            cliente="Empresa X",
            produto="diesel",
            qtd=100,
            cupom=None,
        )
        
        # Configura mocks
        mock_calculo_preco_service.calcular.return_value = 399.0
        mock_desconto_service.aplicar_desconto.return_value = 399.0
        mock_arredondamento_service.arredondar.return_value = 399.0

        # Act
        resultado = use_case.execute(dto)

        # Assert
        assert resultado.sucesso is True
        assert resultado.valor_final == 399.0

    def test_processar_pedido_produto_invalido(
        self,
        mock_calculo_preco_service,
        mock_desconto_service,
        mock_arredondamento_service,
    ):
        """Testa processamento com produto inválido."""
        # Arrange
        use_case = ProcessarPedidoUseCase(
            calculo_preco_service=mock_calculo_preco_service,
            desconto_service=mock_desconto_service,
            arredondamento_service=mock_arredondamento_service,
        )
        
        dto = PedidoInputDTO(
            cliente="Empresa X",
            produto="produto_inexistente",
            qtd=100,
            cupom=None,
        )

        # Act
        resultado = use_case.execute(dto)

        # Assert
        assert resultado.sucesso is False
        assert resultado.valor_final == 0.0
        assert "validação" in resultado.mensagem.lower()

    def test_processar_pedido_quantidade_invalida(
        self,
        mock_calculo_preco_service,
        mock_desconto_service,
        mock_arredondamento_service,
    ):
        """Testa processamento com quantidade inválida."""
        # Arrange
        use_case = ProcessarPedidoUseCase(
            calculo_preco_service=mock_calculo_preco_service,
            desconto_service=mock_desconto_service,
            arredondamento_service=mock_arredondamento_service,
        )
        
        dto = PedidoInputDTO(
            cliente="Empresa X",
            produto="diesel",
            qtd=0,
            cupom=None,
        )

        # Act
        resultado = use_case.execute(dto)

        # Assert
        assert resultado.sucesso is False
        assert resultado.valor_final == 0.0

    def test_processar_pedido_diferentes_produtos(
        self,
        mock_calculo_preco_service,
        mock_desconto_service,
        mock_arredondamento_service,
    ):
        """Testa processamento de diferentes produtos."""
        # Arrange
        use_case = ProcessarPedidoUseCase(
            calculo_preco_service=mock_calculo_preco_service,
            desconto_service=mock_desconto_service,
            arredondamento_service=mock_arredondamento_service,
        )
        
        produtos = ["diesel", "gasolina", "etanol", "lubrificante"]
        
        for produto in produtos:
            # Configura mocks
            mock_calculo_preco_service.calcular.return_value = 100.0
            mock_desconto_service.aplicar_desconto.return_value = 90.0
            mock_arredondamento_service.arredondar.return_value = 90.0
            
            dto = PedidoInputDTO(
                cliente="Empresa X",
                produto=produto,
                qtd=10,
                cupom=None,
            )
            
            # Act
            resultado = use_case.execute(dto)
            
            # Assert
            assert resultado.sucesso is True
            assert resultado.produto == produto
