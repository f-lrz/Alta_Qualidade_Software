# PetroBahia S.A.

A **PetroBahia S.A.** é uma empresa fictícia do setor de óleo e gás. Seu sistema interno calcula preços de combustíveis, valida clientes e gera relatórios. 
O código está **mal estruturado** e **difícil de manter**. O objetivo é **refatorar** aplicando **PEP8**, **Clean Code** e **princípios SOLID** (SRP e OCP).

## Objetivos
- Melhorar legibilidade e clareza do código
- Extrair funções e classes coesas
- Eliminar duplicações e efeitos colaterais
- Melhorar nomes e modularidade

## Estrutura
```
src/
├── main.py
└── legacy/
    ├── clientes.py
    ├── pedido_service.py
    └── preco_calculadora.py
```

## Instruções
1. Leia o código legado.
2. Liste os problemas encontrados.
3. Refatore sem mudar o comportamento principal.
4. Documente suas **decisões de design** neste README.

---

## DECISÕES DE DESIGN
    
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
