# CI/CD Configuration

Este diretório contém os workflows de CI/CD para o projeto AngoData API.

## Workflows Disponíveis

### 1. CI/CD Pipeline (`ci.yml`)
**Triggers:** Push e Pull Request para branches `main` e `develop`

**Jobs:**
- **Test**: Executa testes, linting e análise de código
  - Roda em Python 3.11 e 3.12
  - Black (formatação)
  - isort (organização de imports)
  - Flake8 (linting)
  - Pytest com cobertura de código
  - Codecov (upload de cobertura)
  - Bandit (análise de segurança)
  - Safety (vulnerabilidades em dependências)

- **Build**: Cria imagem Docker (apenas em push para `main`)
  - Docker Buildx
  - Push para Docker Hub
  - Cache otimizado

- **Deploy**: Deploy para produção (apenas em push para `main`)
  - SSH para servidor
  - Pull do código
  - Restart com docker-compose

### 2. Lint e Formatação (`lint.yml`)
**Triggers:** Pull Request para `main` e `develop`

**Ferramentas:**
- Black - Formatação de código
- isort - Organização de imports
- Flake8 - Análise de código
- Pylint - Análise estática
- MyPy - Type checking
- Bandit - Análise de segurança

### 3. Docker Build & Push (`docker.yml`)
**Triggers:** Release publicado ou push de tags (v*)

**Features:**
- Multi-platform build (amd64, arm64)
- Versionamento semântico
- Metadados automáticos
- Cache otimizado

## Secrets Necessários

Configure estes secrets no GitHub (Settings → Secrets and variables → Actions):

### Docker Hub
```
DOCKER_USERNAME - Seu username do Docker Hub
DOCKER_PASSWORD - Seu token de acesso do Docker Hub
```

### Deploy SSH
```
DEPLOY_HOST - IP ou hostname do servidor
DEPLOY_USER - Usuário SSH
DEPLOY_SSH_KEY - Chave privada SSH (conteúdo completo)
DEPLOY_PORT - Porta SSH (padrão: 22)
```

## Como Configurar

### 1. Docker Hub
```bash
# Criar token de acesso no Docker Hub
# https://hub.docker.com/settings/security

# Adicionar secrets no GitHub
# Settings → Secrets and variables → Actions → New repository secret
```

### 2. Deploy SSH
```bash
# Gerar chave SSH (se não tiver)
ssh-keygen -t ed25519 -C "github-actions"

# Copiar chave pública para servidor
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server

# Copiar chave PRIVADA e adicionar como secret DEPLOY_SSH_KEY
cat ~/.ssh/id_ed25519
```

### 3. Codecov (Opcional)
```bash
# Registrar projeto em https://codecov.io
# Token será adicionado automaticamente para repos públicos
# Para repos privados, adicionar CODECOV_TOKEN nos secrets
```

## Rodando Localmente

### Testes
```bash
# Instalar dependências de desenvolvimento
pip install -r requirements.txt

# Rodar testes
pytest tests/ -v --cov=src

# Com cobertura HTML
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

### Linting
```bash
# Black
black --check src/ tests/

# Formatar automaticamente
black src/ tests/

# isort
isort --check-only src/ tests/

# Organizar automaticamente
isort src/ tests/

# Flake8
flake8 src/ tests/

# Pylint
pylint src/

# MyPy
mypy src/

# Bandit (segurança)
bandit -r src/
```

### Docker
```bash
# Build local
docker build -t angodata-api:local .

# Rodar
docker run -p 5001:5001 --env-file .env angodata-api:local

# Docker Compose (recomendado)
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Parar
docker-compose down
```

## Estrutura de Branches

```
main (produção)
  ↑
  └── develop (desenvolvimento)
        ↑
        └── feature/nome-da-feature
        └── bugfix/nome-do-bug
        └── hotfix/nome-do-hotfix
```

### Workflow Recomendado

1. **Feature/Bugfix:**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/minha-feature
   
   # Fazer mudanças
   git add .
   git commit -m "feat: adicionar nova funcionalidade"
   git push origin feature/minha-feature
   
   # Criar Pull Request para develop
   ```

2. **Release:**
   ```bash
   # Após testes em develop
   git checkout main
   git merge develop
   git tag v1.0.0
   git push origin main --tags
   
   # CI/CD fará deploy automático
   ```

3. **Hotfix:**
   ```bash
   git checkout main
   git checkout -b hotfix/bug-critico
   
   # Corrigir bug
   git commit -m "fix: corrigir bug crítico"
   git push origin hotfix/bug-critico
   
   # Merge para main E develop
   ```

## Status Badges

Adicione ao README.md:

```markdown
![CI/CD](https://github.com/anilp07x/angodata-api/workflows/CI/CD%20Pipeline/badge.svg)
![Lint](https://github.com/anilp07x/angodata-api/workflows/Lint%20e%20Formatação/badge.svg)
![Coverage](https://codecov.io/gh/anilp07x/angodata-api/branch/main/graph/badge.svg)
```

## Monitoramento

### GitHub Actions
- Acesse: `https://github.com/anilp07x/angodata-api/actions`
- Veja status de cada workflow
- Logs detalhados de cada step

### Codecov
- Acesse: `https://codecov.io/gh/anilp07x/angodata-api`
- Veja cobertura de código
- Tendências ao longo do tempo

### Docker Hub
- Acesse: `https://hub.docker.com/r/<username>/angodata-api`
- Veja imagens publicadas
- Downloads e estatísticas

## Troubleshooting

### Build Docker falha
```bash
# Verificar Dockerfile localmente
docker build -t test .

# Verificar secrets
# GitHub → Settings → Secrets → Verificar DOCKER_USERNAME e DOCKER_PASSWORD
```

### Deploy SSH falha
```bash
# Testar conexão SSH local
ssh -i ~/.ssh/id_ed25519 user@server

# Verificar formato da chave privada no secret
# Deve começar com: -----BEGIN OPENSSH PRIVATE KEY-----
# Deve incluir toda a chave, incluindo cabeçalhos e quebras de linha
```

### Testes falham
```bash
# Rodar localmente para debug
pytest tests/ -vv --tb=short

# Com logs
pytest tests/ -vv -s

# Teste específico
pytest tests/test_auth.py::test_login -vv
```

## Melhores Práticas

1. **Sempre criar Pull Request** - Nunca push direto para main
2. **Testes passando** - PR só deve ser merged se CI estiver verde
3. **Code Review** - Pelo menos 1 aprovação antes de merge
4. **Mensagens de commit** - Usar conventional commits (feat:, fix:, docs:, etc)
5. **Versionamento** - Seguir SemVer (major.minor.patch)
6. **Documentação** - Atualizar docs junto com código
7. **Segurança** - Nunca commitar secrets ou .env files

## Links Úteis

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Hub](https://hub.docker.com)
- [Codecov](https://codecov.io)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [SemVer](https://semver.org/)
