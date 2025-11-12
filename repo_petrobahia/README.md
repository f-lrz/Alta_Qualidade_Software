# 🏭 PetroBahia S.A. - Sistema de Pedidos

A **PetroBahia S.A.** é uma empresa fictícia do setor de óleo e gás. Seu sistema interno calcula preços de combustíveis, valida clientes e gera relatórios. 

## 🎯 Objetivo do Projeto

Este repositório demonstra a **evolução** de um código legado para uma arquitetura moderna e escalável, aplicando:
- **Clean Code**
- **Princípios SOLID**
- **Clean Architecture**

## 📂 Estrutura do Repositório

```
repo_petrobahia/
├── src/
│   ├── clean_architecture/     ✨ NOVA IMPLEMENTAÇÃO (RECOMENDADO)
│   │   ├── domain/            # Regras de negócio puras
│   │   ├── application/       # Casos de uso
│   │   ├── infrastructure/    # Implementações concretas
│   │   ├── presentation/      # Controllers
│   │   ├── di/               # Dependency Injection
│   │   ├── main.py           # Ponto de entrada
│   │   ├── README.md         # Documentação completa
│   │   ├── COMPARISON.md     # Comparação antes/depois
│   │   └── USAGE_GUIDE.md    # Guia de uso
│   │
│   ├── petrobahia/            # Refatoração intermediária (SOLID)
│   ├── legacy/                # Código legado original
│   └── main.py               # Versão original
│
└── README.md                  # Este arquivo
```

## 🚀 Como Usar

### Executar a Versão Clean Architecture (Recomendado) ⭐

```bash
cd src
python clean_architecture/main.py
```

### Executar os Testes

```bash
cd src
python test_clean_architecture.py
```

### Ver o Diagrama da Arquitetura

```bash
cd src/clean_architecture
python ARCHITECTURE_DIAGRAM.py
```

## 📚 Documentação Detalhada

- 📖 [Clean Architecture - README Completo](src/clean_architecture/README.md)
- 📊 [Comparação Antes/Depois](src/clean_architecture/COMPARISON.md)
- 🔧 [Guia de Uso e Extensão](src/clean_architecture/USAGE_GUIDE.md)

## 🎓 Evolução do Projeto

### 1️⃣ Código Legado (`legacy/`)
- ❌ Código monolítico em um arquivo
- ❌ Acoplamento alto
- ❌ Difícil de testar
- ❌ Difícil de manter

### 2️⃣ Refatoração com SOLID (`petrobahia/`)
- ✅ Separação de responsabilidades
- ✅ Princípios SOLID aplicados
- ✅ Strategy Pattern
- ✅ Dependency Injection básica
- ⚠️ Ainda sem separação clara de camadas

### 3️⃣ Clean Architecture (`clean_architecture/`) ⭐ **RECOMENDADO**
- ✅ Arquitetura em camadas bem definidas
- ✅ Regra de dependência rigorosa
- ✅ Testabilidade máxima
- ✅ Independência de frameworks
- ✅ Código profissional e escalável

## 🎯 Princípios SOLID Aplicados

### S - Single Responsibility Principle ✅
Cada classe tem uma única responsabilidade bem definida.

### O - Open/Closed Principle ✅
Aberto para extensão, fechado para modificação.

### L - Liskov Substitution Principle ✅
Implementações podem ser substituídas sem quebrar o código.

### I - Interface Segregation Principle ✅
Interfaces pequenas e específicas.

### D - Dependency Inversion Principle ✅
Dependência de abstrações, não de implementações concretas.

## 📊 Benefícios da Clean Architecture

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Testabilidade** | Difícil | Fácil |
| **Manutenibilidade** | Baixa | Alta |
| **Extensibilidade** | Difícil | Fácil |
| **Acoplamento** | Alto | Baixo |
| **Coesão** | Baixa | Alta |

## 🔄 Fluxo de Dados (Clean Architecture)

```
Presentation  ──┐
                │
Infrastructure ─┼──> Application ──> DOMAIN (núcleo)
                │
DI Container ───┘
```

## 💡 Conceitos Demonstrados

- **Clean Architecture**: Separação em camadas independentes
- **SOLID**: Todos os 5 princípios aplicados
- **Design Patterns**: Strategy, Repository, Dependency Injection, DTO
- **Domain-Driven Design**: Entidades, Value Objects, Domain Services
- **Testabilidade**: Uso de mocks e interfaces
- **Injeção de Dependência**: Container DI como Composition Root

## 🎓 Referências

- [Clean Architecture - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)

---

## DECISÕES DE DESIGN (Refatoração Intermediária)
    
Para resolver os problemas de violação dos princípios SOLID e Clean Code encontrados no código legado, as seguintes decisões de design foram tomadas na refatoração:

1. Aplicação do Princípio da Responsabilidade Única (SRP)
O código legado misturava várias responsabilidades em poucas funções (ex: cadastrar_cliente validava, persistia e notificava). A refatoração dividiu essas responsabilidades em classes focadas:

Módulo de Clientes (petrobahia/clientes.py):

ClienteValidator: Responsável apenas por validar os dados. A lógica de "aceitar email inválido" foi removida para garantir a integridade.

ClienteRepository: Interface e implementação (ClienteFileRepository) responsáveis apenas por persistir os dados (escrever no arquivo).

NotificationService: Interface e implementação (PrintNotificationService) responsáveis apenas por notificar o usuário (o antigo print de boas-vindas).

ClienteService: Atua como um orquestrador, chamando as três classes acima na ordem correta.

Módulo de Pedidos (petrobahia/pedidos.py):

O PedidoService foi transformado em um orquestrador. Ele não calcula mais preços nem aplica descontos diretamente; ele delega essas tarefas para serviços especializados, quebrando as responsabilidades do legacy/pedido_service.py.

2. Aplicação do Princípio Aberto/Fechado (OCP) com Strategy Pattern
As longas cadeias de if/else (em preco_calculadora.py e pedido_service.py) foram substituídas pelo Padrão de Design Strategy. Isso torna o sistema "Aberto para Extensão, Fechado para Modificação".

Cálculo de Preço (petrobahia/calculos.py): Foi criada uma interface CalculoPrecoStrategy e classes concretas para cada produto (CalculoDieselStrategy, CalculoGasolinaStrategy, etc.). O PrecoCalculadora agora apenas seleciona a estratégia correta.

Benefício: Para adicionar um novo combustível (ex: "Querosene"), basta criar uma nova classe CalculoQueroseneStrategy e registrá-la, sem nenhuma modificação no código existente.

Descontos e Arredondamento (descontos.py, arredondamento.py): A mesma abordagem foi usada. Foram criadas estratégias para cupons (DescontoMega10Strategy) e para regras de arredondamento (ArredondamentoDieselStrategy).

3. Centralização do Domínio e Remoção de "Magic Strings"
Foi criado o arquivo petrobahia/domain.py para centralizar as regras de negócio.

Enums: As "magic strings" (ex: "diesel", "MEGA10") foram substituídas por Enumerações (ProdutoTipo, CupomTipo), melhorando a legibilidade e evitando erros de digitação.

Exceções: Foi definida uma exceção customizada (ValidacaoError) para um fluxo de erro mais claro.

Constantes: Os preços base foram movidos para BASES_PRECO neste arquivo.

4. Injeção de Dependência (DI) e "Composition Root"
As classes de serviço (PedidoService, ClienteService) não criam mais suas próprias dependências (como o PrecoCalculadora). Em vez disso, elas as recebem prontas no construtor (__init__).

O arquivo main_refatorado.py agora age como a "Raiz de Composição" (Composition Root). Ele é o único lugar responsável por "montar" a aplicação: ele instancia as estratégias, os repositórios e os validadores, e os injeta nos serviços que precisam deles. Isso desacopla totalmente os componentes.
