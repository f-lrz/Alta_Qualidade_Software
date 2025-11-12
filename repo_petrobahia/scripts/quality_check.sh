#!/bin/bash

# Script para executar verificações de qualidade de código
# Autor: PetroBahia S.A.
# Uso: ./scripts/quality_check.sh [comando]

set -e  # Parar em caso de erro

PROJECT_DIR="/workspaces/Alta_Qualidade_Software/repo_petrobahia"
TARGET_DIR="src/clean_architecture"

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🔍 PetroBahia - Quality Check Tools"
echo "===================================="
echo ""

# Função para executar Black
run_black() {
    echo -e "${YELLOW}📝 Executando Black (Code Formatter)...${NC}"
    black $TARGET_DIR
    echo -e "${GREEN}✅ Black concluído!${NC}\n"
}

# Função para executar isort
run_isort() {
    echo -e "${YELLOW}📦 Executando isort (Import Sorter)...${NC}"
    isort $TARGET_DIR
    echo -e "${GREEN}✅ isort concluído!${NC}\n"
}

# Função para executar Pylint
run_pylint() {
    echo -e "${YELLOW}🔎 Executando Pylint (Code Analyzer)...${NC}"
    pylint $TARGET_DIR --output-format=text || true
    echo -e "${GREEN}✅ Pylint concluído!${NC}\n"
}

# Função para executar tudo
run_all() {
    echo -e "${YELLOW}🚀 Executando todas as ferramentas...${NC}\n"
    run_black
    run_isort
    run_pylint
}

# Função para verificar sem modificar
check_only() {
    echo -e "${YELLOW}👀 Verificando código (sem modificar)...${NC}\n"
    
    echo -e "${YELLOW}📝 Black - Verificando formatação...${NC}"
    black $TARGET_DIR --check --diff || true
    
    echo -e "\n${YELLOW}📦 isort - Verificando imports...${NC}"
    isort $TARGET_DIR --check-only --diff || true
    
    echo -e "\n${YELLOW}🔎 Pylint - Analisando código...${NC}"
    pylint $TARGET_DIR --output-format=text || true
}

# Menu de comandos
case "${1:-all}" in
    black)
        run_black
        ;;
    isort)
        run_isort
        ;;
    pylint)
        run_pylint
        ;;
    all)
        run_all
        ;;
    check)
        check_only
        ;;
    help)
        echo "Comandos disponíveis:"
        echo "  ./scripts/quality_check.sh black   - Formatar código com Black"
        echo "  ./scripts/quality_check.sh isort   - Organizar imports com isort"
        echo "  ./scripts/quality_check.sh pylint  - Analisar código com Pylint"
        echo "  ./scripts/quality_check.sh all     - Executar todas as ferramentas (padrão)"
        echo "  ./scripts/quality_check.sh check   - Verificar sem modificar"
        echo "  ./scripts/quality_check.sh help    - Mostrar esta ajuda"
        ;;
    *)
        echo -e "${RED}❌ Comando inválido: $1${NC}"
        echo "Use './scripts/quality_check.sh help' para ver os comandos disponíveis"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Processo concluído!${NC}"
