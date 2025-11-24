# CI/CD Configurado ✅

## O que foi criado

### GitHub Actions (`.github/workflows/`)

**1. CI Pipeline** (`ci.yml`)
- Roda em: Push e PR para main/develop
- Testa em: Python 3.11 e 3.12
- Executa: Black, isort, Flake8, pytest com cobertura

**2. Code Quality** (`lint.yml`)
- Roda em: Pull Requests
- Executa: Black, isort, Flake8, Bandit

### Templates

- `.github/ISSUE_TEMPLATE/bug_report.md` - Template para reportar bugs
- `.github/ISSUE_TEMPLATE/feature_request.md` - Template para sugerir features
- `.github/PULL_REQUEST_TEMPLATE.md` - Template para Pull Requests

### Configurações

- `.flake8` - Configuração do linter
- `pyproject.toml` - Configuração de Black, isort, pytest, coverage

### Documentação

- `CONTRIBUTING.md` - Guia de contribuição
- `.github/CI.md` - Documentação do CI

## Como usar

### Localmente

```bash
# Formatar código
black src/ tests/
isort src/ tests/

# Verificar código
flake8 src/

# Rodar testes
pytest tests/ -v --cov=src
```

### No GitHub

1. Faça commit e push
2. Abra Pull Request
3. CI executará automaticamente
4. Aguarde os checks passarem (verde ✅)
5. Merge após aprovação

## Próximos passos

1. Faça commit das mudanças:
```bash
git add .
git commit -m "ci: configurar CI/CD com GitHub Actions"
git push origin main
```

2. Acesse GitHub Actions para ver os workflows:
   https://github.com/anilp07x/angodata-api/actions

3. Adicione badges ao README.md:
```markdown
![CI](https://github.com/anilp07x/angodata-api/workflows/CI%20Pipeline/badge.svg)
![Code Quality](https://github.com/anilp07x/angodata-api/workflows/Code%20Quality/badge.svg)
```

Simples e direto! 🎉
