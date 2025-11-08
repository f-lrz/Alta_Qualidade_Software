# Importa os dados originais
from main import pedidos, clientes

# Importa os serviços refatorados
from petrobahia.clientes import (
    ClienteService,
    ClienteValidator,
    ClienteFileRepository,
    PrintNotificationService
)
from petrobahia.pedidos import PedidoService
from petrobahia.calculos import PrecoCalculadora
from petrobahia.descontos import DescontoService
from petrobahia.arredondamento import ArredondamentoService


def main():
    print("==== Início processamento PetroBahia (REFATORADO) ====")

    # --- Configuração de Dependências (Composition Root) ---
    
    # 1. Dependências de Cliente
    cliente_validator = ClienteValidator()
    # Salva em um arquivo diferente para não misturar com o legado
    cliente_repo = ClienteFileRepository(filepath="clientes_refatorado.txt")
    notification_svc = PrintNotificationService()
    
    # 2. Serviço de Cliente (com dependências injetadas)
    cliente_service = ClienteService(
        validator=cliente_validator,
        repository=cliente_repo,
        notifier=notification_svc
    )
    
    # 3. Dependências de Pedido
    preco_calculadora = PrecoCalculadora()
    desconto_svc = DescontoService()
    arredondamento_svc = ArredondamentoService()

    # 4. Serviço de Pedido (com dependências injetadas)
    pedido_service = PedidoService(
        calculadora=preco_calculadora,
        desconto_svc=desconto_svc,
        arredondamento_svc=arredondamento_svc
    )

    # --- Execução da Lógica de Negócio ---

    # Processar Clientes
    for c in clientes:
        ok = cliente_service.cadastrar_cliente(c)
        if ok:
            print(f"cliente ok: {c['nome']}")
        else:
            print(f"cliente com problema: {c}")

    # Processar Pedidos
    valores = []
    for p in pedidos:
        v = pedido_service.processar_pedido(p)
        valores.append(v)
        print(f"pedido: {p}, -- valor final: {v}")

    print(f"TOTAL = {sum(valores)}")
    print("==== Fim processamento PetroBahia (REFATORADO) ====")

if __name__ == "__main__":
    main()