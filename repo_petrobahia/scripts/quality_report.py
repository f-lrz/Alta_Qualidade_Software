#!/usr/bin/env python3
"""
Relatório de Qualidade de Código - PetroBahia S.A.
Gera um relatório visual das ferramentas de qualidade aplicadas.
"""

import subprocess
import sys
from pathlib import Path


def print_header(text: str):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_section(title: str):
    """Imprime título de seção"""
    print(f"\n{'─' * 70}")
    print(f"  🔹 {title}")
    print(f"{'─' * 70}\n")


def run_command(cmd: list, description: str) -> tuple:
    """Executa comando e retorna resultado"""
    print(f"⏳ {description}...")
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=False, cwd=Path(__file__).parent.parent
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)


def main():
    """Função principal"""
    print_header("📊 RELATÓRIO DE QUALIDADE DE CÓDIGO - PETROBAHIA S.A.")

    target = "src/clean_architecture"

    # Black
    print_section("BLACK - Code Formatter")
    code, stdout, stderr = run_command(
        ["black", target, "--check", "--quiet"], "Verificando formatação"
    )
    if code == 0:
        print("✅ Todos os arquivos estão formatados corretamente!")
    else:
        print("⚠️  Alguns arquivos precisam de formatação")
        print(f"Execute: black {target}")

    # isort
    print_section("ISORT - Import Organizer")
    code, stdout, stderr = run_command(
        ["isort", target, "--check-only", "--quiet"], "Verificando imports"
    )
    if code == 0:
        print("✅ Todos os imports estão organizados!")
    else:
        print("⚠️  Alguns imports precisam de organização")
        print(f"Execute: isort {target}")

    # Pylint
    print_section("PYLINT - Code Analyzer")
    code, stdout, stderr = run_command(
        ["pylint", target, "--output-format=text"], "Analisando código"
    )

    # Extrair score do output
    score = "N/A"
    for line in stdout.split("\n"):
        if "Your code has been rated at" in line:
            score = line.split("at ")[1].split("/")[0].strip()
            break

    print(f"📊 Score: {score}/10")

    if float(score) >= 9.0:
        print("✅ Excelente! Código de alta qualidade!")
    elif float(score) >= 8.0:
        print("✅ Muito bom! Código com boa qualidade!")
    elif float(score) >= 7.0:
        print("⚠️  Bom, mas há espaço para melhorias")
    else:
        print("❌ Código precisa de melhorias significativas")

    # Resumo
    print_section("RESUMO")
    print("📦 Ferramentas Aplicadas:")
    print("  • Black 24.10.0   - Formatador automático")
    print("  • isort 5.13.2    - Organizador de imports")
    print("  • Pylint 3.3.1    - Analisador de código")
    print("\n📝 Configurações:")
    print("  • pyproject.toml  - Black e isort")
    print("  • .pylintrc       - Pylint")
    print("  • .vscode/        - Integração IDE")
    print("\n🚀 Para corrigir problemas:")
    print("  ./scripts/quality_check.sh all")

    print("\n" + "=" * 70)
    print("  ✨ Análise concluída!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
