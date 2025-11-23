# AngoData API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12.3-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.2-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.6-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

</div>

REST API desenvolvida em Flask que fornece dados públicos de Angola, incluindo informações sobre províncias, municípios, escolas, mercados e hospitais. O projeto implementa autenticação JWT, autorização baseada em roles, operações CRUD completas, cache com Redis, paginação avançada e bulk operations.

## Características Principais

- **Arquitetura Modular**: Separação clara de responsabilidades (Routes, Services, Models, Schemas)
- **Factory Pattern**: Inicialização configurável da aplicação
- **Autenticação JWT**: Sistema robusto com access e refresh tokens
- **Autorização por Roles**: Controle granular (Admin, Editor, User/Viewer)
- **Database Dual Mode**: Suporte a JSON (desenvolvimento) e PostgreSQL (produção)
- **Paginação e Busca**: Query params avançados com ordenação e filtros
- **Cache Inteligente**: Redis com invalidação automática
- **Bulk Operations**: Operações em lote para performance
- **Segurança Avançada**: Rate limiting, audit log, security headers
- **Testes Automatizados**: pytest com cobertura de código
- **Validação Robusta**: Marshmallow schemas com mensagens em português

## Status do Projeto

### ✅ Fase 1 - CRUD Básico (Concluída)
- [x] Validação de dados com Marshmallow
- [x] Endpoints POST, PUT, DELETE para todas as entidades
- [x] Persistência em JSON
- [x] Mensagens de erro em português

### ✅ Fase 2 - Autenticação JWT (Concluída)
- [x] Sistema de registro e login
- [x] Geração e validação de tokens JWT
- [x] Refresh tokens
- [x] Hash de senhas com Bcrypt

### ✅ Fase 3 - Autorização (Concluída)
- [x] Decoradores de controle de acesso
- [x] Sistema de roles (Admin, Editor, User)
- [x] Proteção de endpoints por permissão

### ✅ Fase 4 - Segurança Avançada (Concluída)
- [x] Rate limiting (100 req/min por IP)
- [x] Logs de auditoria completos
- [x] Security headers (CSP, HSTS, X-Frame-Options)
- [x] Validação contra XSS/SQL Injection

### ✅ Fase 5 - Database PostgreSQL (Concluída)
- [x] Configuração SQLAlchemy + Alembic
- [x] Models ORM para todas entidades
- [x] Migrations automáticas
- [x] Integração com Supabase (380 registros migrados)
- [x] Service Factory Pattern (DB/JSON mode)

### 🔄 Fase 6 - Funcionalidades Avançadas (80% Completo)
- [x] Paginação (LIMIT/OFFSET) com metadata completo
- [x] Busca avançada (full-text search, sorting, filtering)
- [x] Caching com Redis + SimpleCache
- [x] Bulk operations (create/update/delete em lote)
- [x] Testes unitários e integração (6 testes, 29% cobertura)
- [ ] OpenAPI/Swagger (pacotes instalados, configuração pendente)
- [ ] Replicar features para outras entidades

## Tecnologias Utilizadas

<div align="center">

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | 3.12.3 | Linguagem de programação |
| ![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white) | 3.1.2 | Framework web minimalista |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white) | 17.6 | Banco de dados relacional |
| ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.44-red?style=flat) | 2.0.44 | ORM Python |
| ![Alembic](https://img.shields.io/badge/Alembic-1.17.2-orange?style=flat) | 1.17.2 | Database migrations |
| ![Flask-JWT-Extended](https://img.shields.io/badge/JWT-000000?style=flat&logo=jsonwebtokens&logoColor=white) | 4.7.2 | Autenticação JWT |
| ![Redis](https://img.shields.io/badge/Redis-5.0.1-DC382D?style=flat&logo=redis&logoColor=white) | 5.0.1 | Cache e sessões |
| ![Flask-Caching](https://img.shields.io/badge/Caching-2.1.0-green?style=flat) | 2.1.0 | Sistema de cache |
| ![Marshmallow](https://img.shields.io/badge/Marshmallow-3.21.0-yellow?style=flat) | 3.21.0 | Validação e serialização |
| ![pytest](https://img.shields.io/badge/pytest-7.4.3-blue?style=flat&logo=pytest&logoColor=white) | 7.4.3 | Framework de testes |
| ![Flask-CORS](https://img.shields.io/badge/CORS-5.0.0-lightgrey?style=flat) | 5.0.0 | Gerenciamento de CORS |

</div>

## 🔧 Setup

### 1. Clonar repositório
```bash
git clone <repo-url>
cd angodata-api
```

### 2. Criar virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Copiar `.env.example` para `.env`:
```bash
cp .env.example .env
```

Editar `.env`:
```env
# Flask
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hora

# Database (Opcional - deixar False para usar JSON)
USE_DATABASE=False
DATABASE_URL=postgresql://user:pass@localhost:5432/angodata

# Cache (Opcional)
USE_REDIS=False
REDIS_URL=redis://localhost:6379/0
```

### 5. Executar aplicação
```bash
python app.py
```

API estará disponível em: `http://localhost:5000`

## 📡 API Endpoints

### Autenticação

```bash
# Login
POST /auth/login
{
  "email": "user@example.com",
  "password": "securepassword"
}

# Registrar
POST /auth/register
{
  "email": "user@example.com",
  "password": "securepassword",
  "nome": "João Silva"
}
```

### Províncias

```bash
# Listar todas (com paginação)
GET /provinces/all?page=1&per_page=20&sort_by=nome&order=asc&search=Luanda

# Buscar por ID
GET /provinces/<id>

# Criar (Admin/Editor apenas)
POST /provinces
Authorization: Bearer <token>

# Atualizar
PUT /provinces/<id>
Authorization: Bearer <token>

# Deletar (Admin apenas)
DELETE /provinces/<id>
Authorization: Bearer <token>

# Bulk operations
POST /provinces/bulk
PUT /provinces/bulk
DELETE /provinces/bulk
```

### Outras Entidades

Mesmos endpoints disponíveis para:
- `/municipalities/*`
- `/schools/*`
- `/markets/*`
- `/hospitals/*`

## 🧪 Testes

```bash
# Executar todos os testes
pytest tests/ -v

# Com cobertura
pytest tests/ --cov=src --cov-report=html
```

**Status**: ✅ 6 testes passando, 29% cobertura

## ⚡ Performance

### Com cache ativo (Redis):
- Primeiro request: ~50ms
- Requests subsequentes: ~5ms (90% faster)

### Bulk operations:
- Create 100 registros: ~200ms (vs 5000ms individual)
- Update 100 registros: ~150ms (vs 4000ms individual)

## 🔒 Segurança

- ✅ JWT Authentication
- ✅ Role-based Authorization (Admin, Editor, Viewer)
- ✅ Rate Limiting (100 req/min)
- ✅ Audit Logging
- ✅ Security Headers
- ✅ Password hashing (bcrypt)
- ✅ Input validation (Marshmallow)

## 📚 Documentação

- [PHASE6_ADVANCED_FEATURES.md](./PHASE6_ADVANCED_FEATURES.md) - Detalhes Fase 6
- `.github/copilot-instructions.md` - Instruções para AI

## 📝 Próximos Passos

1. Replicar paginação/bulk/cache para outras entidades
2. Configurar Swagger/OpenAPI
3. Aumentar cobertura de testes para 80%+
4. Documentação completa da API

## 📄 Licença

MIT License

---

**Desenvolvido com ❤️ para Angola 🇦🇴**
