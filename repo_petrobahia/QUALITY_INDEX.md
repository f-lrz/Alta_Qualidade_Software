# 📋 Índice - Ferramentas de Qualidade de Código

## 📁 Estrutura de Arquivos

```
repo_petrobahia/
├── 📝 Configurações
│   ├── requirements-dev.txt        # Dependências (Black, isort, Pylint)
│   ├── pyproject.toml              # Config Black + isort
│   ├── .pylintrc                   # Config Pylint
│   ├── .gitignore                  # Arquivos ignorados
│   ├── .pre-commit-config.yaml     # Hooks CI/CD (opcional)
│   └── .vscode/
│       └── settings.json           # Integração VS Code
│
├── 🔧 Scripts
│   ├── quality_check.sh            # Executar ferramentas (bash)
│   ├── quality_report.py           # Relatório visual (Python)
│   └── quality_demo.py             # Demo para apresentação
│
└── 📚 Documentação
    ├── QUALITY_TOOLS.md            # Guia completo (6.5 KB)
    ├── QUALITY_SUMMARY.md          # Resumo executivo (4.6 KB)
    ├── QUALITY_INDEX.md            # Este arquivo
    └── README.md                   # Atualizado com badges
```

## 🚀 Guia Rápido de Uso

### 1. Instalação (Uma vez)
```bash
pip install -r requirements-dev.txt
```

### 2. Durante Desenvolvimento
- **VS Code**: Formato automático ao salvar (F5)
- **Manual**: `./scripts/quality_check.sh all`

### 3. Antes de Commit
```bash
# Verificar sem modificar
./scripts/quality_check.sh check

# Corrigir problemas
./scripts/quality_check.sh all

# Gerar relatório
python scripts/quality_report.py
```

### 4. Para Apresentação
```bash
# Demo visual
python scripts/quality_demo.py
```

## 📖 Documentação por Tópico

### Para Iniciantes
1. **QUALITY_SUMMARY.md** - Comece aqui! Resumo executivo
2. **README.md** - Visão geral do projeto com badges

### Para Desenvolvedores
1. **QUALITY_TOOLS.md** - Guia completo e detalhado
2. **scripts/quality_check.sh** - Automação diária
3. **.vscode/settings.json** - Integração IDE

### Para Apresentação
1. **QUALITY_SUMMARY.md** - Slides executivos
2. **scripts/quality_demo.py** - Demonstração visual
3. **scripts/quality_report.py** - Relatório ao vivo

### Para DevOps/CI
1. **.pre-commit-config.yaml** - Hooks automáticos
2. **pyproject.toml** - Configuração centralizada
3. **scripts/quality_check.sh** - Script para pipelines

## 🎯 Comandos Essenciais

```bash
# Executar tudo
./scripts/quality_check.sh all

# Apenas verificar (sem modificar)
./scripts/quality_check.sh check

# Ferramenta específica
./scripts/quality_check.sh black
./scripts/quality_check.sh isort
./scripts/quality_check.sh pylint

# Relatórios
python scripts/quality_report.py      # Relatório detalhado
python scripts/quality_demo.py        # Demo para apresentação

# Ajuda
./scripts/quality_check.sh help
```

## 📊 Resultados Atuais

| Ferramenta | Score | Descrição |
|------------|-------|-----------|
| Black | 100% | Todos arquivos formatados |
| isort | 100% | Todos imports organizados |
| Pylint | 8.74/10 | Código de boa qualidade |

## 🔗 Links Úteis

### Documentação Oficial
- [Black](https://black.readthedocs.io/)
- [isort](https://pycqa.github.io/isort/)
- [Pylint](https://pylint.pycqa.org/)

### Documentação Local
- [Guia Completo](QUALITY_TOOLS.md)
- [Resumo Executivo](QUALITY_SUMMARY.md)
- [README Principal](README.md)

## ✅ Checklist de Qualidade

Antes de cada commit:

- [ ] Código formatado com Black (`./scripts/quality_check.sh black`)
- [ ] Imports organizados com isort (`./scripts/quality_check.sh isort`)
- [ ] Score Pylint ≥ 8.0/10 (`./scripts/quality_check.sh pylint`)
- [ ] Testes passando (`python test_clean_architecture.py`)
- [ ] Sem warnings críticos

## 🎓 Treinamento Sugerido

### Nível 1: Básico (30 min)
1. Ler **QUALITY_SUMMARY.md**
2. Executar `./scripts/quality_check.sh all`
3. Ver diferenças no código

### Nível 2: Intermediário (1 hora)
1. Ler **QUALITY_TOOLS.md** completo
2. Configurar VS Code
3. Praticar com código real

### Nível 3: Avançado (2 horas)
1. Entender **pyproject.toml** e **.pylintrc**
2. Customizar regras
3. Integrar com CI/CD

## 🆘 Troubleshooting

### Problema: Script não executa
```bash
# Tornar executável
chmod +x scripts/quality_check.sh
chmod +x scripts/quality_report.py
chmod +x scripts/quality_demo.py
```

### Problema: Import errors no Pylint
✅ Já configurado no `.pylintrc` com `init-hook`

### Problema: Black e isort conflitam
✅ Já configurado: isort usa `profile = "black"`

## 📞 Suporte

- **Documentação**: QUALITY_TOOLS.md
- **Issues**: Verificar README.md
- **Demo**: python scripts/quality_demo.py

---

**Última atualização**: Novembro 2025  
**Mantido por**: PetroBahia S.A. - Equipe de Engenharia
