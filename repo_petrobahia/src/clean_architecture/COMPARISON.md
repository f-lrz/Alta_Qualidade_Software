# 📊 Comparação: Código Original vs Clean Architecture

## Estrutura do Projeto

### ❌ Antes (Código Original)
```
src/
├── main.py                    # Tudo misturado em um arquivo
├── legacy/
│   ├── clientes.py           # Lógica de cliente
│   ├── pedido_service.py     # Lógica de pedido
│   └── preco_calculadora.py  # Cálculos
└── petrobahia/               # Refatoração inicial (ainda acoplado)
```

### ✅ Depois (Clean Architecture)
```
clean_architecture/
├── domain/                    # Regras de negócio puras
│   ├── entities/             # Cliente, Pedido
│   ├── value_objects/        # Enums, constantes
│   ├── exceptions/           # Exceções de domínio
│   ├── repositories/         # Interfaces
│   └── services/             # Interfaces de serviços
├── application/               # Casos de uso
│   ├── use_cases/
│   └── dto/
├── infrastructure/            # Implementações concretas
│   ├── persistence/
│   ├── notification/
│   └── services/
├── presentation/              # Controllers
└── di/                       # Dependency Injection
```

## Dependências

### ❌ Antes
```python
# Código legado - Dependências hardcoded
def processar_pedido(pedido):
    # Abre arquivo diretamente aqui
    with open("clientes.txt", "a") as f:
        f.write(...)
    
    # Cálculos misturados com lógica
    if produto == "diesel":
        preco = 3.99 * qtd
        # ...
```

**Problemas:**
- ❌ Impossível testar sem arquivo real
- ❌ Não pode trocar implementação
- ❌ Lógica de negócio misturada com infraestrutura
- ❌ Alto acoplamento

### ✅ Depois
```python
# Clean Architecture - Inversão de Dependência
class CadastrarClienteUseCase:
    def __init__(
        self,
        cliente_repository: ClienteRepositoryInterface,  # Interface!
        notification_service: NotificationServiceInterface  # Interface!
    ):
        self.cliente_repository = cliente_repository
        self.notification_service = notification_service
```

**Benefícios:**
- ✅ Fácil testar com mocks
- ✅ Pode trocar implementação facilmente
- ✅ Lógica de negócio isolada
- ✅ Baixo acoplamento

## Testabilidade

### ❌ Antes
```python
# Difícil de testar - precisa de arquivo real
def test_processar_pedido():
    # Precisa criar arquivo real
    # Precisa limpar após teste
    # Testa infraestrutura junto com lógica
    resultado = processar_pedido({"cliente": "X", ...})
```

### ✅ Depois
```python
# Fácil de testar - usa mocks
def test_use_case():
    # Cria mocks (sem arquivo, banco, etc)
    mock_repo = Mock()
    mock_notif = Mock()
    
    # Testa APENAS a lógica de negócio
    use_case = CadastrarClienteUseCase(mock_repo, mock_notif)
    resultado = use_case.execute(dto)
    
    # Verifica comportamento
    assert resultado.sucesso
    mock_repo.salvar.assert_called_once()
```

## Extensibilidade

### ❌ Antes
Se você quiser mudar de arquivo para banco de dados:
```python
# Antes: Precisa modificar TODA a lógica
def processar_pedido(pedido):
    # Código acoplado ao arquivo
    with open("clientes.txt", "a") as f:  # <- Precisa mudar TUDO isso
        f.write(...)
    
    # Lógica de negócio misturada
    preco = calcular(...)
```

**Impacto:** 
- ❌ Modificar múltiplos arquivos
- ❌ Risco de quebrar lógica de negócio
- ❌ Precisa reescrever testes

### ✅ Depois
Para mudar de arquivo para banco de dados:
```python
# Basta criar uma NOVA implementação da interface
class ClienteDatabaseRepository(ClienteRepositoryInterface):
    def __init__(self, db_connection):
        self.db = db_connection
    
    def salvar(self, cliente: Cliente) -> None:
        self.db.execute("INSERT INTO clientes ...")

# No Container DI, troca a implementação:
def get_cliente_repository(self):
    return ClienteDatabaseRepository(db_connection)  # <- Só muda aqui!
```

**Impacto:**
- ✅ Criar APENAS o novo repositório
- ✅ Lógica de negócio não muda
- ✅ Testes continuam funcionando (usam mocks)

## Manutenibilidade

### ❌ Antes
```python
# Tudo em um único arquivo/função
def processar_pedido(pedido):
    # Validação
    if not pedido["email"].contains("@"):
        ...
    
    # Persistência
    with open("clientes.txt", "a") as f:
        ...
    
    # Cálculo
    if produto == "diesel":
        preco = 3.99 * qtd
        if qtd > 1000:
            preco *= 0.90
    
    # Desconto
    if cupom == "MEGA10":
        preco *= 0.90
    
    # Notificação
    print("enviando email...")
    
    return preco
```

**Problemas:**
- ❌ Função gigante (viola SRP)
- ❌ Difícil entender o que faz
- ❌ Difícil localizar bugs
- ❌ Mudança em uma parte afeta tudo

### ✅ Depois
```python
# Cada responsabilidade em sua classe
class Cliente:  # Entidade
    def _validar(self): ...

class ClienteFileRepository:  # Persistência
    def salvar(self, cliente): ...

class CalculoPrecoService:  # Cálculo
    def calcular(self, produto, qtd): ...

class DescontoService:  # Desconto
    def aplicar_desconto(self, preco, cupom): ...

class PrintNotificationService:  # Notificação
    def enviar_boas_vindas(self, email, nome): ...

class ProcessarPedidoUseCase:  # Orquestração
    def execute(self, dto):
        # Orquestra os serviços
        preco = self.calculo_service.calcular(...)
        preco_com_desconto = self.desconto_service.aplicar(...)
        return preco_final
```

**Benefícios:**
- ✅ Cada classe tem UMA responsabilidade (SRP)
- ✅ Fácil entender o que cada parte faz
- ✅ Fácil localizar e corrigir bugs
- ✅ Mudanças são isoladas

## Exemplo Prático: Adicionar Novo Produto

### ❌ Antes
```python
# Precisa modificar várias partes do código
def calcular_preco(produto, qtd):
    if produto == "diesel":
        # ...
    elif produto == "gasolina":
        # ...
    elif produto == "etanol":
        # ...
    elif produto == "novo_produto":  # <- Adiciona aqui
        # ...
    # Precisa adicionar em múltiplos lugares!
```

### ✅ Depois
```python
# 1. Adiciona o enum
class ProdutoTipo(Enum):
    DIESEL = "diesel"
    GASOLINA = "gasolina"
    ETANOL = "etanol"
    NOVO_PRODUTO = "novo_produto"  # <- Adiciona aqui

# 2. Adiciona preço base
BASES_PRECO = {
    "novo_produto": 10.0,  # <- Adiciona aqui
}

# 3. Adiciona lógica de cálculo (se necessário)
class CalculoPrecoService:
    def calcular(self, produto, qtd):
        if produto == ProdutoTipo.NOVO_PRODUTO:  # <- Adiciona aqui
            return BASES_PRECO["novo_produto"] * qtd
        # ...

# Tudo continua funcionando!
```

## Métricas de Qualidade

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Linhas por arquivo** | 200+ | 50-100 |
| **Responsabilidades por classe** | 5+ | 1 |
| **Acoplamento** | Alto | Baixo |
| **Coesão** | Baixa | Alta |
| **Testabilidade** | Difícil | Fácil |
| **Extensibilidade** | Difícil | Fácil |
| **Manutenibilidade** | Difícil | Fácil |
| **Compreensibilidade** | Baixa | Alta |

## Princípios SOLID Aplicados

### S - Single Responsibility Principle ✅
- Cada classe tem UMA responsabilidade
- `Cliente` apenas valida e armazena dados
- `ClienteFileRepository` apenas persiste
- `CadastrarClienteUseCase` apenas orquestra

### O - Open/Closed Principle ✅
- Aberto para extensão (novas implementações)
- Fechado para modificação (interfaces não mudam)
- Pode adicionar `ClienteDatabaseRepository` sem modificar código existente

### L - Liskov Substitution Principle ✅
- Qualquer implementação de `ClienteRepositoryInterface` funciona
- `ClienteFileRepository` e `ClienteDatabaseRepository` são intercambiáveis

### I - Interface Segregation Principle ✅
- Interfaces pequenas e específicas
- `ClienteRepositoryInterface` tem apenas métodos de persistência
- `NotificationServiceInterface` tem apenas métodos de notificação

### D - Dependency Inversion Principle ✅
- Módulos de alto nível (Use Cases) não dependem de baixo nível
- Ambos dependem de abstrações (interfaces)
- Use Case depende de `ClienteRepositoryInterface`, não de `ClienteFileRepository`

## Conclusão

A Clean Architecture transforma um código legado difícil de manter em um código:
- ✅ **Profissional**: Segue padrões da indústria
- ✅ **Testável**: Fácil criar testes unitários
- ✅ **Manutenível**: Fácil entender e modificar
- ✅ **Extensível**: Fácil adicionar novas funcionalidades
- ✅ **Escalável**: Suporta crescimento do projeto
- ✅ **Flexível**: Fácil trocar implementações
