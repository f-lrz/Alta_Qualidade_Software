# 🧪 Testes Unitários - Clean Architecture PetroBahia

Este diretório contém todos os testes unitários para o projeto Clean Architecture PetroBahia.

## 📋 Estrutura

```
tests/
├── __init__.py                          # Pacote de testes
├── conftest.py                          # Fixtures e configurações pytest
├── test_domain_entities.py              # Testes das entidades (Cliente, Pedido)
├── test_domain_value_objects.py         # Testes dos value objects e exceções
├── test_application_use_cases.py        # Testes dos casos de uso
├── test_infrastructure_services.py      # Testes dos serviços de infraestrutura
└── test_presentation_controllers.py     # Testes dos controllers
```

## 🎯 Cobertura de Testes

| Camada | Arquivo | Testes | Status |
|--------|---------|--------|--------|
| **Domain** | `test_domain_entities.py` | 15 | ✅ |
| **Domain** | `test_domain_value_objects.py` | 17 | ✅ |
| **Application** | `test_application_use_cases.py` | 9 | ✅ |
| **Infrastructure** | `test_infrastructure_services.py` | 22 | ✅ |
| **Presentation** | `test_presentation_controllers.py` | 9 | ✅ |
| **Total** | | **72** | ✅ |

## 🚀 Como Executar

### Todos os testes
```bash
pytest tests/ -v
```

### Teste específico
```bash
pytest tests/test_domain_entities.py -v
```

### Com relatório HTML
```bash
pytest tests/ --html=pytest_report.html --self-contained-html
```

### Com cobertura
```bash
pytest tests/ --cov=src/clean_architecture --cov-report=html
```

### Comando completo (relatório + cobertura)
```bash
pytest tests/ -v --html=pytest_report.html --self-contained-html \
  --cov=src/clean_architecture --cov-report=html --cov-report=term-missing
```

## 📝 Fixtures Disponíveis

Definidas em `conftest.py`:

- `mock_cliente_repository` - Mock do repositório de clientes
- `mock_notification_service` - Mock do serviço de notificação
- `mock_calculo_preco_service` - Mock do serviço de cálculo de preço
- `mock_desconto_service` - Mock do serviço de desconto
- `mock_arredondamento_service` - Mock do serviço de arredondamento
- `cliente_valido` - Fixture de cliente válido
- `pedido_valido` - Fixture de pedido válido

## 🎓 Padrões Utilizados

### Arrange-Act-Assert (AAA)
```python
def test_exemplo(self):
    # Arrange - Preparar dados e dependências
    cliente = Cliente(nome="João", email="joao@test.com", cnpj="123")
    
    # Act - Executar ação
    resultado = cliente.nome
    
    # Assert - Verificar resultado
    assert resultado == "João"
```

### Mocking
```python
def test_com_mock(self, mock_repository):
    # Configurar mock
    mock_repository.salvar.return_value = True
    
    # Usar mock
    service = ClienteService(repository=mock_repository)
    service.cadastrar(cliente)
    
    # Verificar chamadas
    mock_repository.salvar.assert_called_once()
```

### Testes Parametrizados
```python
@pytest.mark.parametrize("produto,esperado", [
    (ProdutoTipo.DIESEL, 3.99),
    (ProdutoTipo.GASOLINA, 5.19),
])
def test_parametrizado(self, produto, esperado):
    assert BASES_PRECO[produto.value] == esperado
```

## 📊 Métricas

- **Total de Testes**: 72
- **Taxa de Sucesso**: 100%
- **Tempo de Execução**: ~0.65s
- **Cobertura de Código**: 54%
  - Domínio: 100%
  - Aplicação: 95%
  - Infraestrutura: 96%
  - Apresentação: 100%

## 🔍 Detalhamento dos Testes

### 1. Testes de Domínio

#### Entidades (`test_domain_entities.py`)
- Validação de dados de entrada
- Regras de negócio
- Exceções customizadas
- Propriedades computadas

#### Value Objects (`test_domain_value_objects.py`)
- Enums e valores
- Constantes
- Hierarquia de exceções

### 2. Testes de Aplicação

#### Use Cases (`test_application_use_cases.py`)
- Fluxo de cadastro de cliente
- Fluxo de processamento de pedido
- Tratamento de erros
- Integração entre camadas (com mocks)

### 3. Testes de Infraestrutura

#### Serviços (`test_infrastructure_services.py`)
- Cálculo de preços com descontos por volume
- Aplicação de cupons de desconto
- Regras de arredondamento por produto

### 4. Testes de Apresentação

#### Controllers (`test_presentation_controllers.py`)
- Orquestração de múltiplas operações
- Tratamento de falhas parciais
- Cálculo de totais
- Logging de resultados

## 🛠️ Dependências

```bash
pytest==9.0.1
pytest-html==4.1.1
pytest-cov==7.0.0
```

## 📈 Melhorias Futuras

- [ ] Testes de integração end-to-end
- [ ] Testes da camada de persistência
- [ ] Testes de performance/benchmark
- [ ] Testes de carga
- [ ] Property-based testing com Hypothesis
- [ ] Mutation testing com mutpy

## 📚 Referências

- [Pytest Documentation](https://docs.pytest.org/)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Test-Driven Development](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
