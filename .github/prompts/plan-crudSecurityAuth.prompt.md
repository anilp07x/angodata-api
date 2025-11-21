# Plan: Implementação de CRUD Completo, Segurança e Autenticação

**TL;DR:** Transformar a API read-only atual em uma API REST completa com CRUD, autenticação JWT, validação de dados e segurança em camadas. Implementação faseada preservando a arquitetura modular existente (Factory + Blueprints + Services), mantendo compatibilidade com dados in-memory antes da migração para banco de dados.

## Steps

### 1. Configurar validação e segurança
Instalar dependências (Flask-JWT-Extended, Marshmallow, Bcrypt, python-dotenv), criar schemas de validação em `src/schemas/` para todas as entidades, configurar variáveis de ambiente em `.env` com SECRET_KEY e JWT_SECRET_KEY seguros.

### 2. Implementar autenticação JWT
Criar `src/models/user.py` com estrutura de usuário (id, username, email, password_hash, role), implementar `src/services/auth_service.py` com métodos de registro, login, hash de senha (bcrypt) e geração de tokens, adicionar `src/routes/auth.py` com endpoints `/auth/register` e `/auth/login`.

### 3. Adicionar operações CRUD
Estender todos os services (`province_service.py`, `municipality_service.py`, `school_service.py`, `market_service.py`, `hospital_service.py`) com métodos `create()`, `update()`, `delete()`, adicionar rotas POST/PUT/DELETE em cada blueprint, implementar validação com schemas Marshmallow antes de processar dados.

### 4. Proteger rotas com autorização
Criar decorator personalizado `@role_required(['admin'])` em `src/utils/decorators.py`, aplicar `@jwt_required()` em rotas de escrita (POST/PUT/DELETE), permitir leitura (GET) pública ou com autenticação opcional, implementar sistema de roles (admin pode tudo, user apenas leitura).

### 5. Implementar persistência e segurança adicional
Adicionar serialização JSON automática em `src/database/json_storage.py` para persistir dados in-memory entre restarts, configurar Flask-Limiter para rate limiting (ex: 100 requisições/hora por IP), adicionar Flask-Talisman para HTTPS enforcement e security headers, configurar CORS específico por origem em produção.

### 6. Preparar migração para banco de dados
Criar modelos SQLAlchemy em `src/models/` espelhando estruturas atuais, configurar Flask-Migrate para gestão de schemas, criar script de migração `scripts/migrate_data.py` para transferir dados in-memory para PostgreSQL, documentar processo de switch (in-memory → database) com feature flags.

## Further Considerations

### Estratégia de IDs
Atualmente IDs são hardcoded (1-326 para municípios). Para CRUD, considerar:
- **(A) Auto-increment manual** com `max(id) + 1`
- **(B) UUIDs** para prevenir colisões
- **(C) Aguardar migração DB** para usar sequences

**Recomendação:** Opção A para fase in-memory, migrar para C com PostgreSQL.

### Validação de relacionamentos
Schools/Markets/Hospitals referenciam `municipio_id` e `provincia_id`. Ao criar/atualizar, validar:
- **(A) IDs existem** nas tabelas pai
- **(B) Município pertence** à província especificada
- **(C) Implementar cascade delete** ou block delete

**Recomendação:** Validação estrita + block delete até DB migration com foreign keys.

### Níveis de acesso
Definir granularidade de permissões:
- **(A) Simples:** `admin` (CRUD completo) vs `user` (apenas leitura)
- **(B) Moderado:** adicionar `editor` (pode criar/editar, não deletar)
- **(C) Avançado:** permissões por entidade (admin_schools, editor_hospitals)

**Recomendação:** Começar com Opção A, evoluir conforme necessidade.

## Arquitetura Atual (Preservar)

### Padrões Existentes
- **Factory Pattern:** `create_app(config_name)` para diferentes ambientes
- **Blueprints:** Organização modular por entidade (`/provinces`, `/municipalities`, etc.)
- **Three-Layer:** Routes → Services → Models
- **Response Format:** `{"success": bool, "data": any, "total": int, "message": str}`
- **Idioma:** Todas as mensagens em português

### Estrutura de Dados Atual

**Province (21 registros):**
```python
{
    "id": int,
    "nome": str,
    "capital": str,
    "area_km2": float,
    "populacao": int
}
```

**Municipality (326 registros):**
```python
{
    "id": int,
    "nome": str,
    "provincia_id": int,
    "provincia_nome": str
}
```

**School (8 registros):**
```python
{
    "id": int,
    "nome": str,
    "tipo": str,
    "provincia_id": int,
    "provincia_nome": str,
    "municipio_id": int,
    "municipio": str,
    "endereco": str
}
```

**Market (7 registros):**
```python
{
    "id": int,
    "nome": str,
    "tipo": str,
    "provincia_id": int,
    "provincia_nome": str,
    "municipio_id": int,
    "municipio": str,
    "especialidade": str
}
```

**Hospital (9 registros):**
```python
{
    "id": int,
    "nome": str,
    "tipo": str,
    "categoria": str,
    "provincia_id": int,
    "provincia_nome": str,
    "municipio_id": int,
    "municipio": str,
    "endereco": str
}
```

## Dependências Necessárias

### Já Instaladas
```
Flask==3.1.2
Flask-CORS==5.0.0
Werkzeug==3.1.3
```

### A Instalar (Fase 1 - CRUD + Auth)
```
Flask-JWT-Extended==4.6.0
marshmallow==3.21.0
Flask-Marshmallow==1.2.0
Flask-Bcrypt==1.0.1
python-dotenv==1.0.1
```

### A Instalar (Fase 2 - Segurança)
```
Flask-Limiter==3.5.0
Flask-Talisman==1.1.0
```

### A Instalar (Fase 3 - Database)
```
Flask-SQLAlchemy==3.1.1
psycopg2-binary==2.9.9
Flask-Migrate==4.0.7
```

## Endpoints Propostos

### Autenticação
```
POST   /auth/register          # Registro de usuário
POST   /auth/login             # Login (retorna JWT)
POST   /auth/refresh           # Renovar token
POST   /auth/logout            # Invalidar token
GET    /auth/me                # Dados do usuário logado
```

### Províncias (Provinces)
```
GET    /provinces/all          # ✅ Existente - Listar todas
GET    /provinces/<id>         # ✅ Existente - Buscar por ID
POST   /provinces              # 🆕 Criar província [ADMIN]
PUT    /provinces/<id>         # 🆕 Atualizar província [ADMIN]
DELETE /provinces/<id>         # 🆕 Deletar província [ADMIN]
```

### Municípios (Municipalities)
```
GET    /municipalities/all                    # ✅ Existente - Listar todos
GET    /municipalities/<id>                   # ✅ Existente - Buscar por ID
GET    /municipalities?provincia_id=<id>     # 🆕 Filtrar por província
POST   /municipalities                        # 🆕 Criar município [ADMIN]
PUT    /municipalities/<id>                   # 🆕 Atualizar município [ADMIN]
DELETE /municipalities/<id>                   # 🆕 Deletar município [ADMIN]
```

### Escolas (Schools)
```
GET    /schools/all                    # ✅ Existente - Listar todas
GET    /schools/<id>                   # ✅ Existente - Buscar por ID
GET    /schools?provincia_id=<id>     # 🆕 Filtrar por província
GET    /schools?municipio_id=<id>     # 🆕 Filtrar por município
POST   /schools                        # 🆕 Criar escola [ADMIN/EDITOR]
PUT    /schools/<id>                   # 🆕 Atualizar escola [ADMIN/EDITOR]
DELETE /schools/<id>                   # 🆕 Deletar escola [ADMIN]
```

### Mercados (Markets)
```
GET    /markets/all                    # ✅ Existente - Listar todos
GET    /markets/<id>                   # ✅ Existente - Buscar por ID
GET    /markets?provincia_id=<id>     # 🆕 Filtrar por província
GET    /markets?municipio_id=<id>     # 🆕 Filtrar por município
POST   /markets                        # 🆕 Criar mercado [ADMIN/EDITOR]
PUT    /markets/<id>                   # 🆕 Atualizar mercado [ADMIN/EDITOR]
DELETE /markets/<id>                   # 🆕 Deletar mercado [ADMIN]
```

### Hospitais (Hospitals)
```
GET    /hospitals/all                    # ✅ Existente - Listar todos
GET    /hospitals/<id>                   # ✅ Existente - Buscar por ID
GET    /hospitals?provincia_id=<id>     # 🆕 Filtrar por província
GET    /hospitals?municipio_id=<id>     # 🆕 Filtrar por município
POST   /hospitals                        # 🆕 Criar hospital [ADMIN/EDITOR]
PUT    /hospitals/<id>                   # 🆕 Atualizar hospital [ADMIN/EDITOR]
DELETE /hospitals/<id>                   # 🆕 Deletar hospital [ADMIN]
```

## Regras de Negócio

### Autenticação
1. Tokens JWT expiram em 24 horas
2. Refresh tokens expiram em 30 dias
3. Senhas devem ter mínimo 8 caracteres
4. Email deve ser único no sistema
5. Username deve ser único no sistema

### Autorização
1. **Rotas públicas (sem auth):** GET em todas as entidades
2. **Rotas protegidas (user logado):** GET /auth/me
3. **Rotas admin:** POST/PUT/DELETE em provinces e municipalities
4. **Rotas admin/editor:** POST/PUT em schools, markets, hospitals
5. **Rotas apenas admin:** DELETE em schools, markets, hospitals

### Validação de Dados
1. **Province:** nome (required, max 100), capital (required), area_km2 (positive), populacao (positive)
2. **Municipality:** nome (required, max 100), provincia_id (must exist)
3. **School:** nome (required), tipo (enum: Pública/Privada), municipio_id (must exist)
4. **Market:** nome (required), tipo (enum: Formal/Informal), municipio_id (must exist)
5. **Hospital:** nome (required), tipo (enum: Público/Privado), categoria (enum: Geral/Central/Especializado/Pediátrico), municipio_id (must exist)

### Integridade Referencial
1. Ao criar escola/mercado/hospital, validar que municipio_id existe
2. Ao criar município, validar que provincia_id existe
3. Ao deletar província, bloquear se tiver municípios associados
4. Ao deletar município, bloquear se tiver escolas/mercados/hospitais associados
5. Mensagem de erro clara indicando dependências

## Mensagens de Erro (Português)

```python
# Autenticação
"Credenciais inválidas"
"Token expirado"
"Token inválido"
"Acesso negado. Permissões insuficientes"
"Usuário não encontrado"
"Email já está em uso"
"Username já está em uso"
"Senha deve ter no mínimo 8 caracteres"

# Validação
"Campo obrigatório: {field}"
"Valor inválido para {field}"
"{entity} não encontrado(a)"
"ID da província inválido"
"ID do município inválido"

# Integridade
"Não é possível deletar província. Existem {count} municípios associados"
"Não é possível deletar município. Existem dependências (escolas/mercados/hospitais)"
"Município {id} não pertence à província {provincia_id}"

# Rate Limiting
"Limite de requisições excedido. Tente novamente em {seconds} segundos"
```


## Variáveis de Ambiente (.env)

```bash
# Flask
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# JWT
JWT_SECRET_KEY=your-jwt-secret-key-here-change-in-production
JWT_ACCESS_TOKEN_EXPIRES=86400  # 24 horas
JWT_REFRESH_TOKEN_EXPIRES=2592000  # 30 dias

# Database (futuro)
DATABASE_URL=postgresql://user:password@localhost:5432/angodata

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Rate Limiting
RATELIMIT_STORAGE_URL=redis://localhost:6379
RATELIMIT_DEFAULT=100 per hour

# Security
FORCE_HTTPS=False  # True em produção
```

## Estrutura de Arquivos Após Implementação

```
angodata-api/
├── .env                         # 🆕 Variáveis de ambiente
├── .env.example                 # 🆕 Template de .env
├── app.py
├── requirements.txt             # 🔄 Atualizado com novas deps
├── src/
│   ├── __init__.py             # 🔄 Registrar JWT, Limiter
│   ├── config/
│   │   └── config.py           # 🔄 Adicionar configs JWT, DB
│   ├── models/
│   │   ├── __init__.py
│   │   ├── province.py
│   │   ├── municipality.py
│   │   ├── school.py
│   │   ├── market.py
│   │   ├── hospital.py
│   │   └── user.py             # 🆕 Modelo de usuário
│   ├── schemas/                # 🆕 Pasta de schemas Marshmallow
│   │   ├── __init__.py
│   │   ├── province_schema.py
│   │   ├── municipality_schema.py
│   │   ├── school_schema.py
│   │   ├── market_schema.py
│   │   ├── hospital_schema.py
│   │   └── user_schema.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── province_service.py    # 🔄 Adicionar create/update/delete
│   │   ├── municipality_service.py # 🔄 Adicionar create/update/delete
│   │   ├── school_service.py      # 🔄 Adicionar create/update/delete
│   │   ├── market_service.py      # 🔄 Adicionar create/update/delete
│   │   ├── hospital_service.py    # 🔄 Adicionar create/update/delete
│   │   └── auth_service.py        # 🆕 Serviço de autenticação
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── provinces.py           # 🔄 Adicionar POST/PUT/DELETE
│   │   ├── municipalities.py      # 🔄 Adicionar POST/PUT/DELETE
│   │   ├── schools.py             # 🔄 Adicionar POST/PUT/DELETE
│   │   ├── markets.py             # 🔄 Adicionar POST/PUT/DELETE
│   │   ├── hospitals.py           # 🔄 Adicionar POST/PUT/DELETE
│   │   └── auth.py                # 🆕 Rotas de autenticação
│   ├── utils/                     # 🆕 Pasta de utilitários
│   │   ├── __init__.py
│   │   ├── decorators.py          # 🆕 @role_required, etc.
│   │   └── validators.py          # 🆕 Validações customizadas
│   └── database/
│       ├── __init__.py
│       └── json_storage.py        # 🆕 Persistência JSON
├── scripts/                       # 🆕 Scripts utilitários
│   ├── create_admin.py            # 🆕 Criar usuário admin
│   └── migrate_data.py            # 🆕 Migrar para PostgreSQL
├── tests/                         # 🆕 Testes
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_provinces.py
│   ├── test_municipalities.py
│   ├── test_schools.py
│   ├── test_markets.py
│   └── test_hospitals.py
└── venv/
```

## Exemplo de Request/Response

### POST /auth/register
```json
// Request
{
  "username": "admin",
  "email": "admin@angodata.ao",
  "password": "SecurePass123",
  "role": "admin"
}

// Response 201
{
  "success": true,
  "message": "Usuário registrado com sucesso",
  "data": {
    "id": 1,
    "username": "admin",
    "email": "admin@angodata.ao",
    "role": "admin"
  }
}
```

### POST /auth/login
```json
// Request
{
  "email": "admin@angodata.ao",
  "password": "SecurePass123"
}

// Response 200
{
  "success": true,
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@angodata.ao",
      "role": "admin"
    }
  }
}
```

### POST /schools
```json
// Request (com Authorization: Bearer {token})
{
  "nome": "Escola Primária do Cacuaco",
  "tipo": "Pública",
  "provincia_id": 1,
  "municipio_id": 2,
  "endereco": "Bairro Popular, Cacuaco"
}

// Response 201
{
  "success": true,
  "message": "Escola criada com sucesso",
  "data": {
    "id": 9,
    "nome": "Escola Primária do Cacuaco",
    "tipo": "Pública",
    "provincia_id": 1,
    "provincia_nome": "Luanda",
    "municipio_id": 2,
    "municipio": "Cacuaco",
    "endereco": "Bairro Popular, Cacuaco"
  }
}
```

### PUT /schools/9
```json
// Request (com Authorization: Bearer {token})
{
  "endereco": "Bairro Palanca, Cacuaco"
}

// Response 200
{
  "success": true,
  "message": "Escola atualizada com sucesso",
  "data": {
    "id": 9,
    "nome": "Escola Primária do Cacuaco",
    "tipo": "Pública",
    "provincia_id": 1,
    "provincia_nome": "Luanda",
    "municipio_id": 2,
    "municipio": "Cacuaco",
    "endereco": "Bairro Palanca, Cacuaco"
  }
}
```

### DELETE /schools/9
```json
// Request (com Authorization: Bearer {token})
// Sem body

// Response 200
{
  "success": true,
  "message": "Escola deletada com sucesso"
}
```

### Erro: 401 Unauthorized
```json
{
  "success": false,
  "message": "Token inválido ou expirado"
}
```

### Erro: 403 Forbidden
```json
{
  "success": false,
  "message": "Acesso negado. Permissões insuficientes"
}
```

### Erro: 422 Validation Error
```json
{
  "success": false,
  "message": "Erro de validação",
  "errors": {
    "nome": ["Campo obrigatório"],
    "municipio_id": ["ID do município inválido"]
  }
}
```

## Próximos Passos

1. **Revisar e aprovar** este plano
2. **Priorizar fases** conforme cronograma do projeto
3. **Decidir sobre database:** Começar com JSON ou migrar direto para PostgreSQL?
4. **Definir roles:** Apenas admin/user ou incluir editor?
5. **Escolher rate limiting:** Quanto por endpoint?
6. **Configurar ambiente:** Criar .env com chaves seguras
7. **Começar implementação** pela Fase 1

## Questões para Discussão

1. **Usuário inicial:** Como criar primeiro admin sem ter autenticação? (Script `create_admin.py`?)
2. **Roles fixos ou dinâmicos?** Hardcoded ou tabela de permissões?
3. **Soft delete ou hard delete?** Adicionar campo `deleted_at` ou remover permanente?
4. **Auditoria:** Registrar quem criou/modificou cada registro?
5. **Versionamento de API:** Começar com `/api/v1/` ou paths diretos?
6. **Paginação:** Implementar agora ou esperar database?
7. **Cache:** Redis para melhorar performance de leituras?
8. **Testes:** Prioridade alta ou implementar depois?
