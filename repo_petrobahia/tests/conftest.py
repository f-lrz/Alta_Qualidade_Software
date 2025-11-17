"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from unittest.mock import Mock

from clean_architecture.domain.entities import Cliente, Pedido
from clean_architecture.domain.value_objects import ProdutoTipo, CupomTipo
from clean_architecture.domain.repositories import (
    ClienteRepositoryInterface,
    NotificationServiceInterface,
)
from clean_architecture.domain.services import (
    CalculoPrecoServiceInterface,
    DescontoServiceInterface,
    ArredondamentoServiceInterface,
)


@pytest.fixture
def mock_cliente_repository():
    """Mock do repositório de clientes."""
    return Mock(spec=ClienteRepositoryInterface)


@pytest.fixture
def mock_notification_service():
    """Mock do serviço de notificação."""
    return Mock(spec=NotificationServiceInterface)


@pytest.fixture
def mock_calculo_preco_service():
    """Mock do serviço de cálculo de preço."""
    return Mock(spec=CalculoPrecoServiceInterface)


@pytest.fixture
def mock_desconto_service():
    """Mock do serviço de desconto."""
    return Mock(spec=DescontoServiceInterface)


@pytest.fixture
def mock_arredondamento_service():
    """Mock do serviço de arredondamento."""
    return Mock(spec=ArredondamentoServiceInterface)


@pytest.fixture
def cliente_valido():
    """Fixture de cliente válido."""
    return Cliente(nome="João Silva", email="joao@test.com", cnpj="12345678000100")


@pytest.fixture
def pedido_valido():
    """Fixture de pedido válido."""
    return Pedido(
        cliente="Empresa X",
        produto=ProdutoTipo.DIESEL,
        quantidade=100,
        cupom=CupomTipo.MEGA10,
    )
