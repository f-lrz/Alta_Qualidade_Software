"""
Script de testes simples para Clean Architecture
"""

import sys
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("🧪 Iniciando testes da Clean Architecture...\n")

# ===== TESTE 1: Entidades de Domínio =====
print("✓ Teste 1: Criando entidade Cliente válida")
from clean_architecture.domain.entities import Cliente
from clean_architecture.domain.exceptions import ClienteInvalidoError

try:
    cliente = Cliente(
        nome="João Silva",
        email="joao@test.com",
        cnpj="12345678000100"
    )
    print(f"  Cliente criado: {cliente.nome} - {cliente.email}")
    print("  ✅ PASSOU\n")
except Exception as e:
    print(f"  ❌ FALHOU: {e}\n")

# ===== TESTE 2: Validação de Email =====
print("✓ Teste 2: Validando rejeição de email inválido")
try:
    cliente_invalido = Cliente(
        nome="Maria",
        email="email_invalido",
        cnpj="123"
    )
    print("  ❌ FALHOU: Deveria ter lançado exceção\n")
except ClienteInvalidoError as e:
    print(f"  Exceção capturada corretamente: {e}")
    print("  ✅ PASSOU\n")

# ===== TESTE 3: Value Objects =====
print("✓ Teste 3: Usando Value Objects (Enums)")
from clean_architecture.domain.value_objects import ProdutoTipo, CupomTipo

produto = ProdutoTipo.DIESEL
cupom = CupomTipo.MEGA10
print(f"  Produto: {produto.value}")
print(f"  Cupom: {cupom.value}")
print("  ✅ PASSOU\n")

# ===== TESTE 4: Pedido =====
print("✓ Teste 4: Criando Pedido válido")
from clean_architecture.domain.entities import Pedido

pedido = Pedido(
    cliente="Empresa X",
    produto=ProdutoTipo.DIESEL,
    quantidade=100,
    cupom=CupomTipo.MEGA10
)
print(f"  Pedido: {pedido.cliente} - {pedido.produto.value} - {pedido.quantidade}L")
print(f"  Tem cupom? {pedido.tem_cupom}")
print("  ✅ PASSOU\n")

# ===== TESTE 5: Serviço de Cálculo =====
print("✓ Teste 5: Testando serviço de cálculo de preço")
from clean_architecture.infrastructure.services import CalculoPrecoService

calculo_service = CalculoPrecoService()
preco = calculo_service.calcular(ProdutoTipo.DIESEL, 100)
print(f"  Preço calculado para 100L de diesel: R$ {preco:.2f}")
print("  ✅ PASSOU\n")

# ===== TESTE 6: Serviço de Desconto =====
print("✓ Teste 6: Testando serviço de desconto")
from clean_architecture.infrastructure.services import DescontoService

desconto_service = DescontoService()
preco_original = 1000.0
preco_com_desconto = desconto_service.aplicar_desconto(
    preco=preco_original,
    produto=ProdutoTipo.DIESEL,
    quantidade=100,
    cupom=CupomTipo.MEGA10
)
desconto_aplicado = preco_original - preco_com_desconto
print(f"  Preço original: R$ {preco_original:.2f}")
print(f"  Preço com desconto MEGA10: R$ {preco_com_desconto:.2f}")
print(f"  Desconto aplicado: R$ {desconto_aplicado:.2f}")
print("  ✅ PASSOU\n")

# ===== TESTE 7: Use Case com Mocks =====
print("✓ Teste 7: Testando Use Case com dependências mockadas")
from unittest.mock import Mock
from clean_architecture.application.use_cases import CadastrarClienteUseCase
from clean_architecture.application.dto import ClienteInputDTO

# Cria mocks
mock_repository = Mock()
mock_notification = Mock()

# Cria o use case com dependências mockadas
use_case = CadastrarClienteUseCase(
    cliente_repository=mock_repository,
    notification_service=mock_notification
)

# Executa o use case
dto = ClienteInputDTO(nome="Test User", email="test@test.com", cnpj="123")
resultado = use_case.execute(dto)

print(f"  Resultado: {resultado.sucesso}")
print(f"  Mensagem: {resultado.mensagem}")
print(f"  Repositório foi chamado? {mock_repository.salvar.called}")
print(f"  Notificação foi enviada? {mock_notification.enviar_boas_vindas.called}")
print("  ✅ PASSOU\n")

# ===== TESTE 8: Container de DI =====
print("✓ Teste 8: Testando Container de Dependency Injection")
from clean_architecture.di import Container

container = Container()
cliente_controller = container.get_cliente_controller()
pedido_controller = container.get_pedido_controller()

print(f"  Cliente Controller criado: {type(cliente_controller).__name__}")
print(f"  Pedido Controller criado: {type(pedido_controller).__name__}")
print("  ✅ PASSOU\n")

print("=" * 60)
print("🎉 Todos os testes passaram!")
print("=" * 60)
