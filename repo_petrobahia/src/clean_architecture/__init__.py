"""
PetroBahia - Clean Architecture

Organização do projeto seguindo Clean Architecture:

1. Domain Layer (Camada de Domínio)
   - Entidades de negócio
   - Value Objects
   - Exceções de domínio
   - Interfaces de repositórios e serviços
   - Regras de negócio fundamentais

2. Application Layer (Camada de Aplicação)
   - Use Cases (Casos de Uso)
   - DTOs (Data Transfer Objects)
   - Orquestração da lógica de negócio

3. Infrastructure Layer (Camada de Infraestrutura)
   - Implementações de repositórios
   - Serviços externos (email, arquivo, etc)
   - Implementações de serviços de domínio
   - Frameworks e bibliotecas externas

4. Presentation Layer (Camada de Apresentação)
   - Controllers
   - Views/CLI
   - APIs
   - Interface com o usuário

5. DI (Dependency Injection)
   - Container de injeção de dependência
   - Composition Root

Princípios aplicados:
- SOLID (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion)
- Clean Architecture (independência de frameworks, testabilidade, independência de UI)
- Dependency Injection (inversão de controle)
- Strategy Pattern (para cálculos e descontos)
"""

__version__ = "1.0.0"
