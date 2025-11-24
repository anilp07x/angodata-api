# Guia de Contribuição - AngoData API

Obrigado pelo interesse em contribuir com o projeto AngoData API! 🎉

## Código de Conduta

Este projeto adere a um código de conduta. Ao participar, espera-se que você mantenha um ambiente respeitoso e inclusivo.

## Como Contribuir

### 1. Reportar Bugs

Encontrou um bug? Abra uma issue:
1. Use o template de Bug Report
2. Descreva o comportamento esperado vs atual
3. Inclua passos para reproduzir
4. Adicione logs/screenshots se aplicável

### 2. Sugerir Novas Features

Tem uma ideia? Abra uma issue:
1. Use o template de Feature Request
2. Descreva claramente a funcionalidade
3. Explique o problema que resolve

### 3. Contribuir com Código

#### Setup do Ambiente

```bash
# 1. Fork o repositório no GitHub

# 2. Clone seu fork
git clone https://github.com/SEU-USERNAME/angodata-api.git
cd angodata-api

# 3. Adicione o repositório original como upstream
git remote add upstream https://github.com/anilp07x/angodata-api.git

# 4. Crie virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Instale dependências
pip install -r requirements.txt

# 6. Copie .env.example para .env
cp .env.example .env

# 7. Rode testes para verificar
pytest tests/
```

#### Workflow de Desenvolvimento

```bash
# 1. Sincronize com upstream
git checkout main
git pull upstream main

# 2. Crie uma branch para sua feature/fix
git checkout -b feature/nome-da-feature
# ou
git checkout -b bugfix/nome-do-bug

# 3. Faça suas mudanças
# Edite os arquivos necessários

# 4. Execute testes e linting
pytest tests/ -v
black src/ tests/
isort src/ tests/
flake8 src/ tests/

# 5. Commit suas mudanças
git add .
git commit -m "feat: adicionar nova funcionalidade X"
# Use conventional commits (veja abaixo)

# 6. Push para seu fork
git push origin feature/nome-da-feature

# 7. Abra um Pull Request no GitHub
# - Descreva suas mudanças
# - Referencie issues relacionadas
# - Aguarde code review
```

## Padrões de Código

### Conventional Commits

Use mensagens de commit padronizadas:

```
feat: adicionar novo endpoint de busca
fix: corrigir bug no login
docs: atualizar README
style: formatar código
refactor: reorganizar estrutura de services
test: adicionar testes para authentication
chore: atualizar dependências
```

Tipos principais:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (sem mudança de lógica)
- `refactor`: Refatoração de código
- `test`: Adicionar/modificar testes
- `chore`: Tarefas de manutenção

### Python Style Guide

Seguimos **PEP 8** com algumas customizações:

```python
# ✅ Bom
def get_user_by_id(user_id: int) -> dict:
    """
    Busca usuário por ID.
    
    Args:
        user_id: ID do usuário
        
    Returns:
        dict: Dados do usuário
    """
    user = UserService.get_by_id(user_id)
    return user


# ❌ Ruim
def GetUser(id):
    u = UserService.get_by_id(id)
    return u
```

**Regras:**
- Nomes de funções e variáveis: `snake_case`
- Nomes de classes: `PascalCase`
- Constantes: `UPPER_CASE`
- Docstrings em todas as funções/classes
- Type hints quando possível
- Linha máxima: 127 caracteres
- Imports organizados (stdlib, third-party, local)

### Estrutura de Arquivos

```
src/
├── models/          # Modelos de dados
├── services/        # Lógica de negócio
├── routes/          # Endpoints (Blueprints)
├── schemas/         # Validação (Marshmallow)
├── swagger/         # Documentação OpenAPI
├── utils/           # Funções utilitárias
├── database/        # Configuração de DB
└── config/          # Configurações
```

**Ao adicionar código:**
- Coloque no diretório apropriado
- Siga o padrão existente
- Adicione testes correspondentes

### Testes

Todos os PRs devem incluir testes:

```python
# tests/test_feature.py
import pytest

def test_get_all_provinces():
    """Testa busca de todas as províncias"""
    # Arrange
    expected_count = 18
    
    # Act
    provinces = ProvinceService.get_all()
    
    # Assert
    assert len(provinces) == expected_count
    assert all('id' in p for p in provinces)
```

**Cobertura mínima:** 80%

Execute testes antes de abrir PR:
```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Documentação

#### Docstrings

Use Google Style docstrings:

```python
def create_user(username: str, email: str, password: str) -> dict:
    """
    Cria novo usuário no sistema.
    
    Args:
        username: Nome de usuário único
        email: Email válido
        password: Senha (será hasheada)
        
    Returns:
        dict: Dados do usuário criado
        
    Raises:
        ValueError: Se username já existe
        ValidationError: Se dados inválidos
        
    Example:
        >>> user = create_user("joao", "joao@email.com", "senha123")
        >>> print(user['username'])
        'joao'
    """
    # implementação...
```

#### README e Docs

Ao adicionar features, atualize:
- `README.md` - Se mudar funcionalidade principal
- `.github/copilot-instructions.md` - Se mudar arquitetura
- Docstrings - Sempre
- OpenAPI/Swagger - Sempre para novos endpoints

## Checklist de Pull Request

Antes de abrir PR, verifique:

- [ ] Código segue o style guide
- [ ] Todos os testes passam (`pytest`)
- [ ] Cobertura >= 80% (`pytest --cov`)
- [ ] Código formatado (`black`, `isort`)
- [ ] Linting sem erros (`flake8`)
- [ ] Sem vulnerabilidades (`bandit`)
- [ ] Docstrings adicionadas/atualizadas
- [ ] Swagger atualizado (se novo endpoint)
- [ ] README atualizado (se necessário)
- [ ] Conventional commits usado
- [ ] Branch atualizada com main
- [ ] Sem conflitos

## Code Review

### O que esperamos

**Reviewer (quem revisa):**
- Feedback construtivo e respeitoso
- Sugestões de melhoria
- Aprovação se código está bom
- Request changes se houver problemas

**Author (quem submeteu):**
- Responder a todos os comentários
- Fazer mudanças solicitadas
- Explicar decisões técnicas se necessário
- Pedir esclarecimentos se não entender feedback

### Critérios de Aprovação

PR será aprovado se:
- ✅ CI/CD está verde (todos os checks passam)
- ✅ Code review aprovado por pelo menos 1 pessoa
- ✅ Sem conflitos com main
- ✅ Descrição clara do que foi feito
- ✅ Issues relacionadas foram linkadas

## Boas Práticas

### DOs ✅

- Faça commits pequenos e focados
- Escreva mensagens de commit descritivas
- Adicione testes para novo código
- Mantenha cobertura de testes alta
- Documente funções públicas
- Use type hints
- Siga o style guide
- Peça ajuda quando precisar

### DON'Ts ❌

- Não commite código não testado
- Não commite código quebrado
- Não commite secrets (.env, tokens, etc)
- Não faça commits gigantes
- Não ignore code review feedback
- Não force push após PR aberto (sem necessidade)
- Não misture múltiplas features em um PR

## Perguntas Frequentes

### Como atualizar minha branch com main?

```bash
git checkout main
git pull upstream main
git checkout minha-branch
git rebase main
git push --force-with-lease origin minha-branch
```

### Como rodar apenas um teste?

```bash
# Arquivo específico
pytest tests/test_auth.py -v

# Teste específico
pytest tests/test_auth.py::test_login -v
```

## Recursos

- [PEP 8 Style Guide](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## Contato

- **Issues:** [GitHub Issues](https://github.com/anilp07x/angodata-api/issues)
- **Email:** anilpedro07x@outlook.com

---

Obrigado pela sua contribuição! 🚀

