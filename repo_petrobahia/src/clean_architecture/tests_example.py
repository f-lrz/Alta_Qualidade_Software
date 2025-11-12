"""
Testes de Exemplo - Clean Architecture

Este arquivo demonstra como a Clean Architecture facilita os testes.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock

# Adiciona o diretório correto ao path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from application.dto import ClienteInputDTO
from application.use_cases import CadastrarClienteUseCase
from domain.entities import Cliente, Pedido
from domain.exceptions import ClienteInvalidoError
from domain.value_objects import CupomTipo, ProdutoTipo


class TestEntidadeDominio(unittest.TestCase):
    """Testes para entidades de domínio."""

    def test_cliente_valido(self):
        """Testa criação de cliente com dados válidos."""
        cliente = Cliente(
            nome="João Silva", email="joao@test.com", cnpj="12345678000100"
        )
        self.assertEqual(cliente.nome, "João Silva")
        self.assertEqual(cliente.email, "joao@test.com")

    def test_cliente_email_invalido(self):
        """Testa que cliente com email inválido lança exceção."""
        with self.assertRaises(ClienteInvalidoError):
            Cliente(nome="João Silva", email="email_invalido", cnpj="12345678000100")

    def test_pedido_valido(self):
        """Testa criação de pedido válido."""
        pedido = Pedido(
            cliente="Empresa X",
            produto=ProdutoTipo.DIESEL,
            quantidade=100,
            cupom=CupomTipo.MEGA10,
        )
        self.assertEqual(pedido.quantidade, 100)
        self.assertTrue(pedido.tem_cupom)

    def test_pedido_quantidade_invalida(self):
        """Testa que pedido com quantidade inválida lança exceção."""
        with self.assertRaises(ValueError):
            Pedido(
                cliente="Empresa X",
                produto=ProdutoTipo.DIESEL,
                quantidade=0,
                cupom=None,
            )


class TestCadastrarClienteUseCase(unittest.TestCase):
    """Testes para o caso de uso de cadastro de cliente."""

    def setUp(self):
        """Configuração dos mocks."""
        # Mock do repositório
        self.mock_repository = Mock()

        # Mock do serviço de notificação
        self.mock_notification = Mock()

        # Instancia o use case com as dependências mockadas
        self.use_case = CadastrarClienteUseCase(
            cliente_repository=self.mock_repository,
            notification_service=self.mock_notification,
        )

    def test_cadastrar_cliente_sucesso(self):
        """Testa cadastro de cliente com sucesso."""
        # Arrange
        dto = ClienteInputDTO(
            nome="Maria Silva", email="maria@test.com", cnpj="12345678000100"
        )

        # Act
        resultado = self.use_case.execute(dto)

        # Assert
        self.assertTrue(resultado.sucesso)
        self.assertEqual(resultado.nome, "Maria Silva")
        self.mock_repository.salvar.assert_called_once()
        self.mock_notification.enviar_boas_vindas.assert_called_once_with(
            email="maria@test.com", nome="Maria Silva"
        )

    def test_cadastrar_cliente_email_invalido(self):
        """Testa que email inválido retorna erro."""
        # Arrange
        dto = ClienteInputDTO(
            nome="Maria Silva", email="email_invalido", cnpj="12345678000100"
        )

        # Act
        resultado = self.use_case.execute(dto)

        # Assert
        self.assertFalse(resultado.sucesso)
        self.assertIn("Email inválido", resultado.mensagem)
        # Verifica que o repositório NÃO foi chamado
        self.mock_repository.salvar.assert_not_called()
        self.mock_notification.enviar_boas_vindas.assert_not_called()


class TestIsolamentoDeCamadas(unittest.TestCase):
    """
    Testes que demonstram o isolamento das camadas.

    Na Clean Architecture, podemos testar cada camada independentemente
    sem precisar de toda a infraestrutura (banco de dados, arquivo, etc).
    """

    def test_use_case_sem_dependencias_reais(self):
        """
        Demonstra que podemos testar um Use Case sem implementações reais.

        Isso é possível porque o Use Case depende de INTERFACES,
        não de IMPLEMENTAÇÕES concretas.
        """
        # Cria mocks das dependências
        mock_repo = Mock()
        mock_notif = Mock()

        # Injeta os mocks no Use Case
        use_case = CadastrarClienteUseCase(
            cliente_repository=mock_repo, notification_service=mock_notif
        )

        # Testa sem precisar de arquivo, banco de dados, SMTP, etc!
        dto = ClienteInputDTO(nome="Test", email="test@test.com", cnpj="123")
        resultado = use_case.execute(dto)

        # Verifica que funcionou
        self.assertTrue(resultado.sucesso)


def run_tests():
    """Executa todos os testes."""
    # Cria a suite de testes
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Adiciona os testes
    suite.addTests(loader.loadTestsFromTestCase(TestEntidadeDominio))
    suite.addTests(loader.loadTestsFromTestCase(TestCadastrarClienteUseCase))
    suite.addTests(loader.loadTestsFromTestCase(TestIsolamentoDeCamadas))

    # Executa
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    result = run_tests()

    # Retorna código de erro se houver falhas
    sys.exit(0 if result.wasSuccessful() else 1)
