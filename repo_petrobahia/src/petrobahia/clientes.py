import re
from abc import ABC, abstractmethod
from typing import Dict
from .domain import ValidacaoError

# --- Definição de Responsabilidades (SRP) ---

class ClienteValidator:
    """Responsável Apenas por validar os dados do cliente."""
    
    REG_EMAIL = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    def validar(self, cliente: Dict):
        """Valida o dicionário do cliente. Lança ValidacaoError se falhar."""
        if "email" not in cliente or "nome" not in cliente:
            raise ValidacaoError("Campos 'nome' e 'email' são obrigatórios.")
        
        # A regra de "aceitar mesmo se inválido" foi removida.
        # A validação deve ser estrita.
        if not re.match(self.REG_EMAIL, cliente["email"]):
            raise ValidacaoError(f"Email inválido: {cliente['email']}")
        
        # Outras validações (ex: CNPJ) poderiam ir aqui.


class ClienteRepository(ABC):
    """Interface para persistir clientes (SRP)."""
    @abstractmethod
    def salvar(self, cliente: Dict):
        pass

class ClienteFileRepository(ClienteRepository):
    """Implementação concreta que salva em arquivo (SRP)."""
    def __init__(self, filepath: str = "clientes_refatorado.txt"):
        # O caminho não está mais 'hardcoded' dentro da função
        self.filepath = filepath

    def salvar(self, cliente: Dict):
        try:
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(str(cliente) + "\n")
        except IOError as e:
            print(f"Erro ao salvar cliente no arquivo: {e}")
            # Em um app real, lançaria uma exceção de persistência
            raise


class NotificationService(ABC):
    """Interface para notificar usuários (SRP)."""
    @abstractmethod
    def enviar_boas_vindas(self, email: str, nome: str):
        pass

class PrintNotificationService(NotificationService):
    """Implementação concreta que "envia" email via print (SRP)."""
    def enviar_boas_vindas(self, email: str, nome: str):
        # A lógica de "enviar email" está isolada.
        print(f"enviando email de boas vindas para {email} (Cliente: {nome})")


# --- Orquestrador (Service Layer) ---

class ClienteService:
    """Orquestra as operações de cliente, unindo as responsabilidades."""
    
    def __init__(
        self,
        validator: ClienteValidator,
        repository: ClienteRepository,
        notifier: NotificationService
    ):
        self.validator = validator
        self.repository = repository
        self.notifier = notifier

    def cadastrar_cliente(self, cliente: Dict) -> bool:
        """Orquestra o processo de cadastro de cliente."""
        try:
            # 1. Validar
            self.validator.validar(cliente)
            
            # 2. Persistir
            self.repository.salvar(cliente)
            
            # 3. Notificar
            self.notifier.enviar_boas_vindas(cliente["email"], cliente["nome"])
            
            return True
            
        except ValidacaoError as e:
            print(f"Falha na validação: {e}")
            return False
        except Exception as e:
            print(f"Erro inesperado no cadastro: {e}")
            return False