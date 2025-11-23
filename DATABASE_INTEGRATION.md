# Integração PostgreSQL com Supabase

## Overview

A API AngoData agora suporta **dois modos de armazenamento**:

1. **JSON Storage** (modo legado): Dados em arquivos JSON locais
2. **PostgreSQL Database** (novo): Dados em Supabase PostgreSQL 17.6

O sistema usa um **Service Factory Pattern** que permite alternar entre os dois modos através de uma **feature flag** no arquivo `.env`.

## Arquitetura

```
┌─────────────────────────────────────┐
│          Flask Routes               │
│  (provinces, municipalities, etc)   │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│        ServiceFactory               │
│  ┌────────────────────────────┐     │
│  │ if USE_DATABASE == True    │     │
│  │    return ProvinceServiceDB│     │
│  │ else                       │     │
│  │    return ProvinceService  │     │
│  └────────────────────────────┘     │
└─────────────┬──────────┬────────────┘
              │          │
    ┌─────────▼───┐  ┌──▼─────────────┐
    │ DB Services │  │ JSON Services  │
    │ (SQLAlchemy)│  │ (In-Memory)    │
    └─────────┬───┘  └──┬─────────────┘
              │         │
       ┌──────▼─────┐  │
       │ PostgreSQL │  │
       │  Supabase  │  │
       └────────────┘  │
                    ┌──▼─────────┐
                    │ JSON Files │
                    └────────────┘
```

## Configuração

### 1. Variáveis de Ambiente (.env)

Adicione as seguintes variáveis ao arquivo `.env`:

```bash
# Database Configuration
USE_DATABASE=False  # Altere para True para usar PostgreSQL
DATABASE_URL=postgresql://postgres.xvrfipgavouqrlgbfkia:YOUR_PASSWORD_HERE@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### 2. Obter Credenciais do Supabase

1. Acesse [Supabase Dashboard](https://app.supabase.com)
2. Selecione o projeto `angodata-api-database`
3. Vá em **Settings** → **Database**
4. Copie a **Connection String** (modo Connection Pooling)
5. Substitua `YOUR_PASSWORD_HERE` pela senha real

### 3. Estrutura de Dados Migrada

O banco já contém todos os dados migrados do JSON:

| Tabela          | Registros |
|-----------------|-----------|
| users           | 5         |
| provinces       | 26        |
| municipalities  | 326       |
| schools         | 9         |
| markets         | 6         |
| hospitals       | 8         |
| **TOTAL**       | **380**   |

## Uso

### Modo JSON (Padrão)

```bash
# .env
USE_DATABASE=False
```

A API carregará dados dos arquivos JSON em `data/`.

### Modo PostgreSQL

```bash
# .env
USE_DATABASE=True
DATABASE_URL=postgresql://postgres.xvrfipgavouqrlgbfkia:SUA_SENHA@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

A API conectará ao Supabase e usará os ORM services.

## Testando a Integração

### 1. Teste Automatizado

Execute o script de testes:

```bash
./test_database.sh
```

O script valida:
- ✓ Configuração de variáveis de ambiente
- ✓ Conexão com PostgreSQL
- ✓ Contagem de dados (380 registros)
- ✓ ServiceFactory switching
- ✓ Relacionamentos entre entidades
- ✓ CRUD básico

### 2. Teste Manual com Python

```python
from src.database.base import init_database, get_db_session
from src.database.models import Province

# Inicializar database
init_database()

# Query usando sessão
with get_db_session() as session:
    provinces = session.query(Province).all()
    for province in provinces:
        print(province.to_dict())
```

### 3. Teste com API HTTP

```bash
# Iniciar servidor
python app.py

# Testar endpoint (deve retornar dados do PostgreSQL)
curl http://localhost:5000/provinces/all
```

## Services ORM

### Localização

Todos os services baseados em database estão em:

```
src/services/db/
├── __init__.py
├── province_service_db.py
├── municipality_service_db.py
├── school_service_db.py
├── market_service_db.py
├── hospital_service_db.py
└── user_service_db.py
```

### Interface Compatível

Os DB Services mantêm **a mesma interface** dos JSON Services:

```python
# JSON Service
class ProvinceService:
    @staticmethod
    def get_all() -> List[Dict]:
        return PROVINCES

# DB Service (mesma interface)
class ProvinceServiceDB:
    @staticmethod
    def get_all() -> List[Dict]:
        with get_db_session() as session:
            provinces = session.query(Province).all()
            return [p.to_dict() for p in provinces]
```

## Modelos ORM

### Localização

```
src/database/models/__init__.py
```

### Entidades

1. **User**: Autenticação e autorização
   - Campos: id, username, email, password_hash, role, created_at
   - Enum: UserRole (admin, editor, user)

2. **Province**: Províncias de Angola
   - Campos: id, nome, capital, area_km2, populacao
   - Relacionamentos: municipalities, schools, markets, hospitals

3. **Municipality**: Municípios
   - Campos: id, nome, provincia_id, area_km2, populacao
   - FK: provincia_id → provinces.id

4. **School**: Escolas
   - Campos: id, nome, provincia_id, municipio, tipo, nivel
   - FK: provincia_id → provinces.id

5. **Market**: Mercados
   - Campos: id, nome, provincia_id, municipio, tipo, endereco
   - FK: provincia_id → provinces.id

6. **Hospital**: Hospitais
   - Campos: id, nome, provincia_id, municipio, tipo, endereco, especialidades
   - FK: provincia_id → provinces.id

## Migrations com Alembic

### Criar Nova Migration

```bash
# Ativar virtual environment
source venv/bin/activate

# Gerar migration automática
alembic revision --autogenerate -m "Descrição da mudança"

# Aplicar migration
alembic upgrade head
```

### Reverter Migration

```bash
# Reverter última migration
alembic downgrade -1

# Reverter para versão específica
alembic downgrade <revision_id>
```

### Histórico de Migrations

```bash
alembic history
```

## Connection Pooling

O sistema usa **connection pooling** para performance:

```python
# src/database/base.py
engine = create_engine(
    database_url,
    pool_size=10,           # 10 conexões permanentes
    max_overflow=20,        # +20 conexões sob demanda
    pool_pre_ping=True,     # Validar conexões antes de usar
    pool_recycle=3600       # Renovar conexões a cada hora
)
```

## Tratamento de Erros

Todos os services incluem **error handling robusto**:

```python
try:
    with get_db_session() as session:
        # Database operations
        pass
except SQLAlchemyError as e:
    print(f"Database error: {e}")
    return None  # ou []
```

## Performance

### Índices

Todos os campos frequentemente consultados têm índices:

```sql
-- Índices criados
CREATE INDEX idx_provinces_nome ON provinces(nome);
CREATE INDEX idx_municipalities_nome ON municipalities(nome);
CREATE INDEX idx_municipalities_provincia_id ON municipalities(provincia_id);
CREATE INDEX idx_schools_nome ON schools(nome);
CREATE INDEX idx_schools_provincia_id ON schools(provincia_id);
-- ... e outros
```

### Queries Otimizadas

```python
# Ordem alfabética
session.query(Province).order_by(Province.nome).all()

# Filtros eficientes
session.query(Municipality).filter(
    Municipality.provincia_id == province_id
).all()
```

## Troubleshooting

### Erro: "No module named 'psycopg2'"

```bash
pip install psycopg2-binary
```

### Erro: "Connection refused"

Verifique:
1. DATABASE_URL está correto no `.env`
2. Senha do Supabase está correta
3. Firewall permite conexões na porta 6543

### Erro: "Table does not exist"

```bash
# Aplicar migrations
alembic upgrade head
```

Ou use MCP Supabase para recriar tabelas.

### Performance lenta

1. Verifique índices: `\d+ table_name` no psql
2. Aumente pool_size se muitas requisições simultâneas
3. Use `EXPLAIN ANALYZE` para queries lentas

## Próximos Passos - Fase 6

Com o banco de dados configurado, podemos implementar:

1. **Paginação**: Limitar resultados de queries grandes
2. **Busca Avançada**: Filtros e ordenação complexa
3. **Caching**: Redis para queries frequentes
4. **Bulk Operations**: Inserção/atualização em lote
5. **Soft Deletes**: Marcação ao invés de remoção física
6. **Audit Trail**: Histórico de mudanças no database
7. **Full-Text Search**: Busca textual com PostgreSQL

## Recursos

- [Supabase Dashboard](https://app.supabase.com)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [PostgreSQL 17 Docs](https://www.postgresql.org/docs/17/)

