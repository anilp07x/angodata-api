# CI/CD - AngoData API

Configuração simples de CI/CD usando GitHub Actions.

## Workflows

### 1. CI Pipeline (`.github/workflows/ci.yml`)
**Executa em:** Push e Pull Request para `main` e `develop`

**Testes em Python 3.11 e 3.12:**
- ✅ Formatação (Black)
- ✅ Imports (isort)
- ✅ Linting (Flake8)
- ✅ Testes (pytest)
- ✅ Cobertura de código

### 2. Code Quality (`.github/workflows/lint.yml`)
**Executa em:** Pull Request

**Verificações:**
- Black - Formatação de código
- isort - Organização de imports
- Flake8 - Análise de código
- Bandit - Análise de segurança

## Como Usar

### Rodar Testes Localmente

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar testes
pytest tests/ -v --cov=src

# Formatar código
black src/ tests/
isort src/ tests/

# Verificar código
flake8 src/
```

### Workflow de Desenvolvimento

```bash
# 1. Criar branch
git checkout -b feature/minha-feature

# 2. Fazer mudanças
# ... editar arquivos ...

# 3. Formatar e testar
black src/ tests/
pytest tests/

# 4. Commit
git add .
git commit -m "feat: adicionar nova funcionalidade"

# 5. Push
git push origin feature/minha-feature

# 6. Abrir Pull Request no GitHub
# CI será executado automaticamente
```

## Status

Veja o status do CI em: https://github.com/anilp07x/angodata-api/actions

## Badges

Adicione ao README.md:

```markdown
![CI](https://github.com/anilp07x/angodata-api/workflows/CI%20Pipeline/badge.svg)
![Code Quality](https://github.com/anilp07x/angodata-api/workflows/Code%20Quality/badge.svg)
```
