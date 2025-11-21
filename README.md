# AngoData API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12.3-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.2-000000?style=for-the-badge&logo=flask&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

</div>

REST API desenvolvida em Flask que fornece dados públicos de Angola, incluindo informações sobre províncias, municípios, escolas, mercados e hospitais. O projeto implementa autenticação JWT, autorização baseada em roles e operações CRUD completas.

## Características Principais

- Arquitetura modular com separação de responsabilidades (Routes, Services, Models)
- Padrão Factory para inicialização e configuração da aplicação
- Sistema de autenticação e autorização com JWT
- Controle de acesso baseado em roles (Admin, Editor, User)
- Validação de dados com Marshmallow
- Persistência de dados em JSON
- CORS configurável para integração front-end
- Respostas padronizadas em português

## Início Rápido

### Pré-requisitos

- Python 3.12.3 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:

```bash
git clone https://github.com/anilp07x/angodata-api.git
cd angodata-api
```

2. Ative o ambiente virtual:

```bash
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:

Copie o arquivo `.env.example` para `.env` e ajuste as configurações conforme necessário.

5. Execute a aplicação:

```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

## Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação. Para acessar endpoints protegidos, você precisa:

1. Registrar um usuário:

```bash
curl -X POST http://localhost:5001/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "seu_usuario",
    "email": "seu@email.com",
    "password": "sua_senha_segura",
    "role": "user"
  }'
```

2. Fazer login para obter o token:

```bash
curl -X POST http://localhost:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seu@email.com",
    "password": "sua_senha_segura"
  }'
```

3. Usar o token em requisições protegidas:

```bash
curl -X POST http://localhost:5001/provinces \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
  -d '{
    "nome": "Nova Província",
    "capital": "Capital",
    "area_km2": 10000,
    "populacao": 100000
  }'
```

## Endpoints da API

### Autenticação

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/auth/register` | Registrar novo usuário | Não |
| POST | `/auth/login` | Autenticar e obter tokens | Não |
| POST | `/auth/refresh` | Renovar access token | Refresh Token |
| GET | `/auth/me` | Obter dados do usuário atual | Sim |
| GET | `/auth/users` | Listar todos os usuários | Admin |

### Províncias

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/provinces/all` | Listar todas as províncias | Não |
| GET | `/provinces/<id>` | Obter província específica | Não |
| POST | `/provinces` | Criar nova província | Editor/Admin |
| PUT | `/provinces/<id>` | Atualizar província | Editor/Admin |
| DELETE | `/provinces/<id>` | Deletar província | Editor/Admin |

### Municípios

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/municipalities/all` | Listar todos os municípios | Não |
| GET | `/municipalities/<id>` | Obter município específico | Não |
| POST | `/municipalities` | Criar novo município | Editor/Admin |
| PUT | `/municipalities/<id>` | Atualizar município | Editor/Admin |
| DELETE | `/municipalities/<id>` | Deletar município | Editor/Admin |

### Escolas

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/schools/all` | Listar todas as escolas | Não |
| GET | `/schools/<id>` | Obter escola específica | Não |
| POST | `/schools` | Criar nova escola | Editor/Admin |
| PUT | `/schools/<id>` | Atualizar escola | Editor/Admin |
| DELETE | `/schools/<id>` | Deletar escola | Editor/Admin |

### Mercados

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/markets/all` | Listar todos os mercados | Não |
| GET | `/markets/<id>` | Obter mercado específico | Não |
| POST | `/markets` | Criar novo mercado | Editor/Admin |
| PUT | `/markets/<id>` | Atualizar mercado | Editor/Admin |
| DELETE | `/markets/<id>` | Deletar mercado | Editor/Admin |

### Hospitais

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| GET | `/hospitals/all` | Listar todos os hospitais | Não |
| GET | `/hospitals/<id>` | Obter hospital específico | Não |
| POST | `/hospitals` | Criar novo hospital | Editor/Admin |
| PUT | `/hospitals/<id>` | Atualizar hospital | Editor/Admin |
| DELETE | `/hospitals/<id>` | Deletar hospital | Editor/Admin |

## Estrutura do Projeto

```text
angodata-api/
├── app.py                          # Ponto de entrada da aplicação
├── requirements.txt                # Dependências do projeto
├── .env                            # Variáveis de ambiente (não versionado)
├── .env.example                    # Exemplo de configuração
├── scripts/
│   └── create_admin.py            # Script para criar usuário administrador
├── data/                          # Dados persistidos em JSON
│   ├── provinces.json
│   ├── municipalities.json
│   ├── schools.json
│   ├── markets.json
│   ├── hospitals.json
│   └── users.json
└── src/
    ├── __init__.py                # Factory create_app()
    ├── config/
    │   ├── __init__.py
    │   └── config.py              # Configurações por ambiente
    ├── models/                    # Estruturas de dados
    │   ├── __init__.py
    │   ├── province.py
    │   ├── municipality.py
    │   ├── school.py
    │   ├── market.py
    │   ├── hospital.py
    │   └── user.py
    ├── schemas/                   # Validação com Marshmallow
    │   ├── __init__.py
    │   ├── province_schema.py
    │   ├── municipality_schema.py
    │   ├── school_schema.py
    │   ├── market_schema.py
    │   ├── hospital_schema.py
    │   └── user_schema.py
    ├── services/                  # Lógica de negócio
    │   ├── __init__.py
    │   ├── province_service.py
    │   ├── municipality_service.py
    │   ├── school_service.py
    │   ├── market_service.py
    │   ├── hospital_service.py
    │   └── auth_service.py
    ├── routes/                    # Endpoints (Blueprints)
    │   ├── __init__.py
    │   ├── provinces.py
    │   ├── municipalities.py
    │   ├── schools.py
    │   ├── markets.py
    │   ├── hospitals.py
    │   └── auth.py
    ├── database/                  # Persistência
    │   ├── __init__.py
    │   └── json_storage.py
    └── utils/                     # Utilitários
        ├── __init__.py
        ├── decorators.py          # Decoradores de autorização
        └── persistence.py         # Decorador de persistência
```

## Tecnologias Utilizadas

<div align="center">

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | 3.12.3 | Linguagem de programação |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) | 3.1.2 | Framework web minimalista |
| ![Flask-CORS](https://img.shields.io/badge/Flask--CORS-5.0.0-lightgrey?style=flat) | 5.0.0 | Gerenciamento de CORS |
| ![Flask-JWT-Extended](https://img.shields.io/badge/JWT-000000?style=flat&logo=jsonwebtokens&logoColor=white) | 4.6.0 | Autenticação JWT |
| ![Flask-Bcrypt](https://img.shields.io/badge/Bcrypt-1.0.1-orange?style=flat) | 1.0.1 | Hashing de senhas |
| ![Marshmallow](https://img.shields.io/badge/Marshmallow-3.21.0-yellow?style=flat) | 3.21.0 | Validação e serialização |
| ![python-dotenv](https://img.shields.io/badge/dotenv-1.0.1-green?style=flat) | 1.0.1 | Gerenciamento de variáveis de ambiente |

</div>

## Arquitetura

### Padrões de Design

**Factory Pattern**: A aplicação é inicializada através da função `create_app()`, permitindo diferentes configurações para desenvolvimento e produção.

**Three-Layer Architecture**:

1. **Routes (Blueprints)**: Recebem requisições HTTP, validam entrada e retornam respostas
2. **Services**: Contêm a lógica de negócio e manipulação de dados
3. **Models**: Estruturas de dados e estado da aplicação

**Decorator Pattern**: Utilizado para autenticação (`@jwt_required()`), autorização (`@role_required()`) e persistência de dados (`@persist_data`).

### Sistema de Autorização

A API implementa controle de acesso baseado em três níveis de permissão:

| Role | Permissões |
|------|------------|
| **Admin** | Acesso completo: CRUD em todos os recursos + gerenciamento de usuários |
| **Editor** | CRUD em recursos de dados (províncias, municípios, escolas, mercados, hospitais) |
| **User** | Apenas leitura (GET) em recursos públicos |

### Validação de Dados

Todas as entradas são validadas usando schemas Marshmallow com:

- Validação de tipos de dados
- Validação de campos obrigatórios
- Validação de enumerações (ex: tipo de escola, tipo de mercado)
- Mensagens de erro em português

## Formato de Resposta

Todas as respostas da API seguem um formato padronizado:

### Resposta de Sucesso

```json
{
  "success": true,
  "total": 18,
  "data": [...]
}
```

### Resposta de Erro

```json
{
  "success": false,
  "message": "Descrição do erro em português"
}
```

### Resposta de Validação

```json
{
  "success": false,
  "message": "Erro de validação",
  "errors": {
    "campo": ["Mensagem de erro específica"]
  }
}
```

## Desenvolvimento

### Criar Usuário Administrador

Para criar o primeiro usuário administrador, execute:

```bash
python scripts/create_admin.py
```

O script solicitará interativamente:

- Nome de usuário
- Email
- Senha (mínimo 8 caracteres)
- Confirmação de senha

### Executar Testes

```bash
# Testes de autorização
chmod +x test_authorization.sh
./test_authorization.sh
```

### Variáveis de Ambiente

Principais variáveis configuráveis no arquivo `.env`:

```env
# Flask
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui

# JWT
JWT_SECRET_KEY=sua_chave_jwt_aqui
JWT_ACCESS_TOKEN_EXPIRES=86400      # 24 horas
JWT_REFRESH_TOKEN_EXPIRES=2592000   # 30 dias

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5000
```

## Roadmap

### Fase 1 - CRUD Básico (Concluída)

- [x] Validação de dados com Marshmallow
- [x] Endpoints POST, PUT, DELETE para todas as entidades
- [x] Persistência em JSON
- [x] Mensagens de erro em português

### Fase 2 - Autenticação JWT (Concluída)

- [x] Sistema de registro e login
- [x] Geração e validação de tokens JWT
- [x] Refresh tokens
- [x] Hash de senhas com Bcrypt

### Fase 3 - Autorização (Concluída)

- [x] Decoradores de controle de acesso
- [x] Sistema de roles (Admin, Editor, User)
- [x] Proteção de endpoints por permissão

### Fase 4 - Segurança Avançada (Planejada)

- [ ] Rate limiting
- [ ] Logs de auditoria
- [ ] HTTPS enforcement
- [ ] Headers de segurança (CSP, HSTS)
- [ ] Validação adicional contra XSS/SQL Injection

### Fase 5 - Migração para Banco de Dados (Planejada)

- [ ] Configuração SQLAlchemy
- [ ] Models ORM
- [ ] Migrations com Alembic
- [ ] Migração de dados JSON para PostgreSQL
- [ ] Connection pooling

### Fase 6 - Funcionalidades Avançadas (Planejada)

- [ ] Paginação de resultados
- [ ] Filtros e busca avançada
- [ ] Ordenação customizável
- [ ] Documentação OpenAPI/Swagger
- [ ] Testes automatizados (pytest)
- [ ] CI/CD pipeline

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Licença

Este projeto disponibiliza dados públicos de Angola de forma aberta para fins educacionais e de desenvolvimento.

## Contato

Desenvolvido por Anilson Pedro - [@anilp07x](https://github.com/anilp07x)

---

<div align="center">

**AngoData API** - Dados públicos de Angola acessíveis via REST API

</div>
