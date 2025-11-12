# 🚀 Guia de Uso - Clean Architecture PetroBahia

## 📖 Índice
1. [Execução](#execução)
2. [Estrutura](#estrutura)
3. [Exemplos de Uso](#exemplos-de-uso)
4. [Testes](#testes)
5. [Extensão](#extensão)

## 🏃 Execução

### Executar a Aplicação Principal
```bash
cd /workspaces/Alta_Qualidade_Software/repo_petrobahia/src
python clean_architecture/main.py
```

### Executar os Testes
```bash
cd /workspaces/Alta_Qualidade_Software/repo_petrobahia/src
python test_clean_architecture.py
```

### Ver o Diagrama da Arquitetura
```bash
cd /workspaces/Alta_Qualidade_Software/repo_petrobahia/src/clean_architecture
python ARCHITECTURE_DIAGRAM.py
```

## 📂 Estrutura

```
clean_architecture/
├── domain/              # Camada de Domínio (regras de negócio)
├── application/         # Camada de Aplicação (casos de uso)
├── infrastructure/      # Camada de Infraestrutura (implementações)
├── presentation/        # Camada de Apresentação (controllers)
├── di/                  # Injeção de Dependência
├── main.py             # Ponto de entrada
├── README.md           # Documentação completa
├── COMPARISON.md       # Comparação antes/depois
└── ARCHITECTURE_DIAGRAM.py  # Diagrama visual
```

## 💡 Exemplos de Uso

### 1. Cadastrar um Cliente

```python
from clean_architecture.di import Container
from clean_architecture.application.dto import ClienteInputDTO

# Inicializa o container
container = Container()

# Obtém o controller
controller = container.get_cliente_controller()

# Cria o DTO
cliente_dto = ClienteInputDTO(
    nome="João Silva",
    email="joao@email.com",
    cnpj="12345678000100"
)

# Cadastra o cliente
resultado = controller.cadastrar_clientes([cliente_dto])
print(resultado[0].mensagem)
```

### 2. Processar um Pedido

```python
from clean_architecture.di import Container
from clean_architecture.application.dto import PedidoInputDTO

# Inicializa o container
container = Container()

# Obtém o controller
controller = container.get_pedido_controller()

# Cria o DTO
pedido_dto = PedidoInputDTO(
    cliente="Empresa X",
    produto="diesel",
    qtd=1000,
    cupom="MEGA10"
)

# Processa o pedido
resultado = controller.processar_pedidos([pedido_dto])
print(f"Valor: R$ {resultado[0].valor_final:.2f}")
```

### 3. Usar Diretamente os Use Cases (sem Controller)

```python
from clean_architecture.di import Container
from clean_architecture.application.dto import ClienteInputDTO

container = Container()

# Obtém o use case diretamente
use_case = container.get_cadastrar_cliente_use_case()

# Executa
dto = ClienteInputDTO(nome="Maria", email="maria@email.com", cnpj="999")
resultado = use_case.execute(dto)

if resultado.sucesso:
    print("Cliente cadastrado!")
else:
    print(f"Erro: {resultado.mensagem}")
```

## 🧪 Testes

### Testar com Mocks (Sem Dependências Reais)

```python
from unittest.mock import Mock
from clean_architecture.application.use_cases import CadastrarClienteUseCase
from clean_architecture.application.dto import ClienteInputDTO

# Cria mocks das dependências
mock_repository = Mock()
mock_notification = Mock()

# Injeta os mocks
use_case = CadastrarClienteUseCase(
    cliente_repository=mock_repository,
    notification_service=mock_notification
)

# Testa
dto = ClienteInputDTO(nome="Test", email="test@test.com", cnpj="123")
resultado = use_case.execute(dto)

# Verifica
assert resultado.sucesso
assert mock_repository.salvar.called
```

### Testar Entidades de Domínio

```python
from clean_architecture.domain.entities import Cliente
from clean_architecture.domain.exceptions import ClienteInvalidoError

# Teste com dados válidos
cliente = Cliente(nome="João", email="joao@test.com", cnpj="123")
assert cliente.nome == "João"

# Teste com dados inválidos
try:
    cliente_invalido = Cliente(nome="Maria", email="email_invalido", cnpj="123")
except ClienteInvalidoError as e:
    print(f"Validação funcionou: {e}")
```

## 🔧 Extensão

### Adicionar Novo Repositório (Ex: Banco de Dados)

**1. Crie a implementação:**
```python
# infrastructure/persistence/database_repository.py
from domain.repositories import ClienteRepositoryInterface
from domain.entities import Cliente

class ClienteDatabaseRepository(ClienteRepositoryInterface):
    def __init__(self, db_connection):
        self.db = db_connection
    
    def salvar(self, cliente: Cliente) -> None:
        query = "INSERT INTO clientes (nome, email, cnpj) VALUES (?, ?, ?)"
        self.db.execute(query, (cliente.nome, cliente.email, cliente.cnpj))
    
    def buscar_por_email(self, email: str) -> Cliente:
        query = "SELECT * FROM clientes WHERE email = ?"
        row = self.db.execute(query, (email,)).fetchone()
        if row:
            return Cliente(nome=row[0], email=row[1], cnpj=row[2])
        return None
```

**2. Atualize o Container DI:**
```python
# di/container.py
def get_cliente_repository(self):
    if 'cliente_repository' not in self._instances:
        # Troca a implementação aqui!
        db_connection = self._get_database_connection()
        self._instances['cliente_repository'] = ClienteDatabaseRepository(db_connection)
    return self._instances['cliente_repository']
```

**Pronto!** Todo o resto do código continua funcionando sem alterações.

### Adicionar Novo Produto

**1. Adicione o enum:**
```python
# domain/value_objects/__init__.py
class ProdutoTipo(Enum):
    DIESEL = "diesel"
    GASOLINA = "gasolina"
    ETANOL = "etanol"
    LUBRIFICANTE = "lubrificante"
    GNV = "gnv"  # <- Novo produto
```

**2. Adicione o preço base:**
```python
BASES_PRECO = {
    "diesel": 3.99,
    "gasolina": 5.19,
    "etanol": 3.59,
    "lubrificante": 25.0,
    "gnv": 4.50,  # <- Novo preço
}
```

**3. Adicione a lógica de cálculo (se necessário):**
```python
# infrastructure/services/__init__.py
class CalculoPrecoService(CalculoPrecoServiceInterface):
    def calcular(self, produto: ProdutoTipo, quantidade: int) -> float:
        # ... código existente ...
        
        elif produto == ProdutoTipo.GNV:  # <- Nova lógica
            preco = BASES_PRECO["gnv"] * quantidade
            if quantidade > 300:
                preco *= 0.92  # 8% desconto
            return preco
```

### Adicionar Novo Cupom de Desconto

**1. Adicione o enum:**
```python
class CupomTipo(Enum):
    MEGA10 = "MEGA10"
    NOVO5 = "NOVO5"
    LUB2 = "LUB2"
    BLACK20 = "BLACK20"  # <- Novo cupom
```

**2. Adicione a lógica:**
```python
class DescontoService(DescontoServiceInterface):
    def aplicar_desconto(self, preco, produto, quantidade, cupom):
        # ... código existente ...
        
        elif cupom == CupomTipo.BLACK20:  # <- Nova lógica
            return preco * 0.80  # 20% desconto
```

### Adicionar Nova Interface (Ex: API REST)

**1. Crie um novo controller:**
```python
# presentation/api_controller.py
from flask import Flask, jsonify, request
from ..di import Container

app = Flask(__name__)
container = Container()

@app.route('/clientes', methods=['POST'])
def cadastrar_cliente():
    data = request.json
    controller = container.get_cliente_controller()
    
    dto = ClienteInputDTO(
        nome=data['nome'],
        email=data['email'],
        cnpj=data['cnpj']
    )
    
    resultado = controller.cadastrar_clientes([dto])[0]
    
    if resultado.sucesso:
        return jsonify({'sucesso': True, 'cliente': data}), 201
    else:
        return jsonify({'sucesso': False, 'erro': resultado.mensagem}), 400
```

**A lógica de negócio não muda!** Apenas a interface de apresentação.

## 📚 Documentação Adicional

- **README.md**: Documentação completa da arquitetura
- **COMPARISON.md**: Comparação detalhada antes/depois
- **ARCHITECTURE_DIAGRAM.py**: Diagrama visual da arquitetura

## 🎯 Princípios a Seguir

1. **Regra de Dependência**: Sempre aponte para dentro (para o domínio)
2. **SRP**: Uma classe, uma responsabilidade
3. **DIP**: Dependa de interfaces, não de implementações
4. **OCP**: Aberto para extensão, fechado para modificação
5. **Testes**: Sempre use mocks para dependências externas

## 🤝 Contribuindo

Ao adicionar novas funcionalidades:

1. ✅ Defina as interfaces no **domain**
2. ✅ Crie os use cases na **application**
3. ✅ Implemente na **infrastructure**
4. ✅ Exponha via **presentation**
5. ✅ Configure no **DI container**
6. ✅ Escreva testes com mocks

## 📞 Suporte

Para dúvidas sobre Clean Architecture:
- [Clean Architecture (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Dependency Injection Pattern](https://martinfowler.com/articles/injection.html)
