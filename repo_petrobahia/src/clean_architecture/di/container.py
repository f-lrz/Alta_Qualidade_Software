"""
Dependency Injection Container

Responsável por criar e configurar todas as dependências da aplicação.
Este é o Composition Root da aplicação.
"""

from ..application.use_cases import CadastrarClienteUseCase, ProcessarPedidoUseCase
from ..domain.repositories import (
    ClienteRepositoryInterface,
    NotificationServiceInterface,
)
from ..domain.services import (
    ArredondamentoServiceInterface,
    CalculoPrecoServiceInterface,
    DescontoServiceInterface,
)
from ..infrastructure.notification import PrintNotificationService
from ..infrastructure.persistence import ClienteFileRepository
from ..infrastructure.services import (
    ArredondamentoService,
    CalculoPrecoService,
    DescontoService,
)
from ..presentation.cliente_controller import ClienteController
from ..presentation.pedido_controller import PedidoController


class Container:
    """
    Container de Injeção de Dependência.

    Segue o princípio de Inversão de Dependência (DIP):
    - Módulos de alto nível não dependem de módulos de baixo nível
    - Ambos dependem de abstrações (interfaces)
    """

    def __init__(self, config: dict = None):
        """
        Inicializa o container com configurações opcionais.

        Args:
            config: Dicionário com configurações (ex: caminho de arquivos, SMTP, etc)
        """
        self.config = config or {}
        self._instances = {}

    # ===== INFRASTRUCTURE LAYER =====

    def get_cliente_repository(self) -> ClienteRepositoryInterface:
        """Retorna a implementação do repositório de cliente."""
        if "cliente_repository" not in self._instances:
            filepath = self.config.get("cliente_file", "clientes_clean_arch.txt")
            self._instances["cliente_repository"] = ClienteFileRepository(filepath)
        return self._instances["cliente_repository"]

    def get_notification_service(self) -> NotificationServiceInterface:
        """Retorna a implementação do serviço de notificação."""
        if "notification_service" not in self._instances:
            # Pode ser configurado para usar email real ou print
            self._instances["notification_service"] = PrintNotificationService()
        return self._instances["notification_service"]

    def get_calculo_preco_service(self) -> CalculoPrecoServiceInterface:
        """Retorna a implementação do serviço de cálculo de preço."""
        if "calculo_preco_service" not in self._instances:
            self._instances["calculo_preco_service"] = CalculoPrecoService()
        return self._instances["calculo_preco_service"]

    def get_desconto_service(self) -> DescontoServiceInterface:
        """Retorna a implementação do serviço de desconto."""
        if "desconto_service" not in self._instances:
            self._instances["desconto_service"] = DescontoService()
        return self._instances["desconto_service"]

    def get_arredondamento_service(self) -> ArredondamentoServiceInterface:
        """Retorna a implementação do serviço de arredondamento."""
        if "arredondamento_service" not in self._instances:
            self._instances["arredondamento_service"] = ArredondamentoService()
        return self._instances["arredondamento_service"]

    # ===== APPLICATION LAYER =====

    def get_cadastrar_cliente_use_case(self) -> CadastrarClienteUseCase:
        """Retorna o caso de uso de cadastro de cliente."""
        if "cadastrar_cliente_use_case" not in self._instances:
            self._instances["cadastrar_cliente_use_case"] = CadastrarClienteUseCase(
                cliente_repository=self.get_cliente_repository(),
                notification_service=self.get_notification_service(),
            )
        return self._instances["cadastrar_cliente_use_case"]

    def get_processar_pedido_use_case(self) -> ProcessarPedidoUseCase:
        """Retorna o caso de uso de processamento de pedido."""
        if "processar_pedido_use_case" not in self._instances:
            self._instances["processar_pedido_use_case"] = ProcessarPedidoUseCase(
                calculo_preco_service=self.get_calculo_preco_service(),
                desconto_service=self.get_desconto_service(),
                arredondamento_service=self.get_arredondamento_service(),
            )
        return self._instances["processar_pedido_use_case"]

    # ===== PRESENTATION LAYER =====

    def get_cliente_controller(self) -> ClienteController:
        """Retorna o controller de cliente."""
        if "cliente_controller" not in self._instances:
            self._instances["cliente_controller"] = ClienteController(
                cadastrar_cliente_use_case=self.get_cadastrar_cliente_use_case()
            )
        return self._instances["cliente_controller"]

    def get_pedido_controller(self) -> PedidoController:
        """Retorna o controller de pedido."""
        if "pedido_controller" not in self._instances:
            self._instances["pedido_controller"] = PedidoController(
                processar_pedido_use_case=self.get_processar_pedido_use_case()
            )
        return self._instances["pedido_controller"]
