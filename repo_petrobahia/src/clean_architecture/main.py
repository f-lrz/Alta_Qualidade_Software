"""
Main Entry Point - Clean Architecture

Este arquivo é o ponto de entrada da aplicação.
Demonstra como usar a Clean Architecture na prática.
"""

import sys
from pathlib import Path

# Adiciona o diretório src ao path para permitir imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from clean_architecture.di import Container


def main():
    """Função principal da aplicação."""

    print("=" * 60)
    print("🏭 PETROBAHIA - Sistema de Pedidos (Clean Architecture)")
    print("=" * 60)
    print()

    # ===== CONFIGURAÇÃO =====
    # Aqui poderíamos carregar configurações de arquivo, env vars, etc.
    config = {
        "cliente_file": "clientes_clean_arch.txt",
    }

    # ===== COMPOSITION ROOT =====
    # Container de DI que gerencia todas as dependências
    container = Container(config)

    # ===== DADOS DE TESTE =====
    clientes = [
        {"nome": "Ana Paula", "email": "ana@petrobahia.com", "cnpj": "123"},
        {"nome": "Carlos Silva", "email": "carlos@petrobahia.com", "cnpj": "456"},
        {
            "nome": "Maria Santos",
            "email": "maria@@invalid",
            "cnpj": "789",
        },  # Email inválido
    ]

    pedidos = [
        {"cliente": "TransLog", "produto": "diesel", "qtd": 1200, "cupom": "MEGA10"},
        {"cliente": "MoveMais", "produto": "gasolina", "qtd": 300, "cupom": None},
        {"cliente": "EcoFrota", "produto": "etanol", "qtd": 50, "cupom": "NOVO5"},
        {"cliente": "PetroPark", "produto": "lubrificante", "qtd": 12, "cupom": "LUB2"},
    ]

    # ===== PROCESSAMENTO DE CLIENTES =====
    print("📋 PROCESSAMENTO DE CLIENTES")
    print("-" * 60)

    cliente_controller = container.get_cliente_controller()
    resultados_clientes = cliente_controller.cadastrar_clientes(clientes)

    print()

    # ===== PROCESSAMENTO DE PEDIDOS =====
    print("📦 PROCESSAMENTO DE PEDIDOS")
    print("-" * 60)

    pedido_controller = container.get_pedido_controller()
    resultados_pedidos = pedido_controller.processar_pedidos(pedidos)

    print()
    print("=" * 60)
    print("✨ Processamento concluído!")
    print("=" * 60)

    # ===== ESTATÍSTICAS =====
    clientes_ok = sum(1 for r in resultados_clientes if r.sucesso)
    pedidos_ok = sum(1 for r in resultados_pedidos if r.sucesso)

    print()
    print("📊 ESTATÍSTICAS:")
    print(f"   Clientes processados: {clientes_ok}/{len(clientes)}")
    print(f"   Pedidos processados: {pedidos_ok}/{len(pedidos)}")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro fatal: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
