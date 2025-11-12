# PetroBahia - Clean Architecture

## 🏗️ Arquitetura

Este projeto foi reorganizado seguindo os princípios de **Clean Architecture** (Arquitetura Limpa) propostos por Robert C. Martin (Uncle Bob).

## 📁 Estrutura do Projeto

```
clean_architecture/
│
├── domain/                      # Camada de Domínio (Núcleo)
│   ├── entities/               # Entidades de negócio
│   ├── value_objects/          # Objetos de valor (Enums, constantes)
│   ├── exceptions/             # Exceções de domínio
│   ├── repositories/           # Interfaces de repositórios
│   └── services/               # Interfaces de serviços de domínio
│
├── application/                 # Camada de Aplicação
│   ├── use_cases/              # Casos de uso (regras de aplicação)
│   │   ├── cadastrar_cliente.py
│   │   └── processar_pedido.py
│   └── dto/                    # Data Transfer Objects
│
├── infrastructure/              # Camada de Infraestrutura
│   ├── persistence/            # Implementações de repositórios
│   ├── notification/           # Serviços de notificação
│   └── services/               # Implementações de serviços
│
├── presentation/                # Camada de Apresentação
│   ├── cliente_controller.py   # Controller de clientes
│   └── pedido_controller.py    # Controller de pedidos
│
├── di/                          # Dependency Injection
│   └── container.py            # Container de DI (Composition Root)
│
└── main.py                      # Ponto de entrada da aplicação
```

## 🎯 Princípios Aplicados

### 1. SOLID

- **S**ingle Responsibility Principle: Cada classe tem uma única responsabilidade
- **O**pen/Closed Principle: Aberto para extensão, fechado para modificação
- **L**iskov Substitution Principle: Substituição de implementações sem quebrar o código
- **I**nterface Segregation Principle: Interfaces específicas e coesas
- **D**ependency Inversion Principle: Dependência de abstrações, não de implementações

### 2. Clean Architecture

#### Regra de Dependência
As dependências sempre apontam para dentro (das camadas externas para as internas):

```
Presentation → Application → Domain
Infrastructure → Application → Domain
```

A camada de **Domain** não conhece nenhuma outra camada.

#### Camadas

##### 🎯 Domain (Núcleo)
- **Responsabilidade**: Regras de negócio fundamentais
- **Não depende de**: Nada (camada mais interna)
- **Contém**: 
  - Entidades (`Cliente`, `Pedido`)
  - Value Objects (`ProdutoTipo`, `CupomTipo`)
  - Exceções de domínio
  - Interfaces (contratos) de repositórios e serviços

##### 📋 Application
- **Responsabilidade**: Orquestração da lógica de negócio (casos de uso)
- **Depende de**: Domain
- **Contém**: 
  - Use Cases (`CadastrarClienteUseCase`, `ProcessarPedidoUseCase`)
  - DTOs para entrada e saída de dados

##### 🔧 Infrastructure
- **Responsabilidade**: Detalhes técnicos e implementações concretas
- **Depende de**: Domain (implementa as interfaces definidas no domínio)
- **Contém**: 
  - Implementações de repositórios (arquivo, banco de dados, etc)
  - Serviços externos (email, SMS, etc)
  - Implementações de serviços de domínio

##### 🖥️ Presentation
- **Responsabilidade**: Interface com o usuário
- **Depende de**: Application
- **Contém**: 
  - Controllers (CLI, API REST, GraphQL, etc)
  - Views
  - Formatação de dados para exibição

##### 💉 DI (Dependency Injection)
- **Responsabilidade**: Composition Root - criar e conectar todas as dependências
- **Depende de**: Todas as camadas (é o único lugar onde isso é permitido)
- **Contém**: 
  - Container de DI que instancia e injeta dependências

## 🚀 Como Executar

```bash
# Navegar para o diretório
cd /workspaces/Alta_Qualidade_Software/repo_petrobahia/src

# Executar a aplicação
python clean_architecture/main.py
```

## 🧪 Benefícios da Clean Architecture

### 1. **Testabilidade**
- Cada camada pode ser testada independentemente
- Fácil criar mocks e stubs das interfaces
- Testes não dependem de frameworks externos

### 2. **Independência de Frameworks**
- O domínio não conhece frameworks
- Fácil trocar de framework web, ORM, etc
- O negócio é protegido de mudanças tecnológicas

### 3. **Independência de UI**
- A mesma aplicação pode ter CLI, Web, API REST, GraphQL
- Trocar a interface não afeta o negócio

### 4. **Independência de Banco de Dados**
- Fácil trocar de arquivo para SQL, NoSQL, etc
- O domínio não sabe onde os dados são armazenados

### 5. **Manutenibilidade**
- Código organizado e fácil de entender
- Separação clara de responsabilidades
- Fácil localizar onde fazer mudanças

### 6. **Extensibilidade**
- Adicionar novos casos de uso é simples
- Adicionar novas implementações não quebra o existente
- Seguir o princípio Open/Closed

## 📊 Fluxo de Dados

```
┌─────────────────────────────────────────────────────────────┐
│                       PRESENTATION                          │
│  (Controllers - Interface com usuário)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ DTOs
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION                            │
│  (Use Cases - Orquestração da lógica de negócio)           │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ Interfaces
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                        DOMAIN                               │
│  (Entidades, Value Objects, Regras de Negócio)            │
└─────────────────────────────────────────────────────────────┘
                      ▲
                      │ Implementa
                      │
┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE                           │
│  (Repositórios, Serviços Externos, Detalhes Técnicos)     │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Exemplo de Fluxo: Cadastrar Cliente

1. **Presentation**: `ClienteController` recebe dados brutos
2. **Presentation**: Converte para `ClienteInputDTO`
3. **Application**: `CadastrarClienteUseCase` recebe o DTO
4. **Application**: Cria entidade `Cliente` (validação automática)
5. **Infrastructure**: `ClienteFileRepository` salva em arquivo
6. **Infrastructure**: `PrintNotificationService` envia notificação
7. **Application**: Retorna `ClienteOutputDTO` com resultado
8. **Presentation**: Exibe resultado para o usuário

## 🎓 Conceitos Importantes

### Dependency Inversion (Inversão de Dependência)
```python
# ❌ ERRADO: Depender de implementação concreta
class UseCase:
    def __init__(self):
        self.repo = ClienteFileRepository()  # Acoplado!

# ✅ CORRETO: Depender de abstração
class UseCase:
    def __init__(self, repo: ClienteRepositoryInterface):
        self.repo = repo  # Desacoplado!
```

### Composition Root
O `Container` é o único lugar onde as dependências concretas são criadas e conectadas:

```python
container = Container()
cliente_controller = container.get_cliente_controller()
# Todas as dependências são injetadas automaticamente!
```

## 📚 Referências

- [Clean Architecture (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Dependency Injection](https://martinfowler.com/articles/injection.html)

## 📝 Comparação: Antes vs Depois

### Antes (Código Legacy)
- ❌ Código monolítico em um único arquivo
- ❌ Dependências hardcoded
- ❌ Difícil de testar
- ❌ Acoplamento alto
- ❌ Difícil de manter e evoluir

### Depois (Clean Architecture)
- ✅ Separação clara de responsabilidades
- ✅ Dependências injetadas via interfaces
- ✅ Fácil de testar (cada camada isoladamente)
- ✅ Baixo acoplamento
- ✅ Fácil de manter e evoluir
- ✅ Código mais legível e profissional
