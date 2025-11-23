# Configuração do Supabase - Fase 5

## 1. Criar Projeto no Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Faça login ou crie uma conta
3. Clique em "New Project"
4. Preencha:
   - **Name**: `angodata-api`
   - **Database Password**: (anote essa senha!)
   - **Region**: Escolha a mais próxima (ex: South America - São Paulo)
5. Clique em "Create new project"
6. Aguarde ~2 minutos para o projeto ser provisionado

---

## 2. Obter Connection String

### Opção A: Dashboard (Recomendado)

1. No dashboard do projeto, vá para **Settings** (ícone de engrenagem)
2. Clique em **Database** no menu lateral
3. Role até **Connection string**
4. Selecione a aba **URI**
5. Copie a string que começa com `postgresql://postgres...`
6. Substitua `[YOUR-PASSWORD]` pela senha que você criou

### Opção B: Usando MCP Supabase

Se você instalou o MCP do Supabase, pode usar:

```bash
# Obter connection string via MCP
# (comando depende da configuração do seu MCP)
```

---

## 3. Configurar .env

Edite o arquivo `.env` e adicione a connection string:

```bash
# Database
DATABASE_URL=postgresql://postgres:SUA_SENHA_AQUI@db.xxx.supabase.co:5432/postgres
USE_DATABASE=True
```

**Exemplo real:**
```bash
DATABASE_URL=postgresql://postgres:MySecurePass123@db.abcdefghijk.supabase.co:5432/postgres
USE_DATABASE=True
```

---

## 4. Testar Conexão

Execute este comando para testar a conexão:

```bash
python -c "from sqlalchemy import create_engine; import os; from dotenv import load_dotenv; load_dotenv(); engine = create_engine(os.getenv('DATABASE_URL')); conn = engine.connect(); print('✅ Conexão bem-sucedida!'); conn.close()"
```

Se der erro, verifique:
- ✅ Senha correta (sem espaços extras)
- ✅ URL completa copiada
- ✅ Projeto Supabase ativo (não pausado)

---

## 5. Executar Migrations

Após configurar a DATABASE_URL:

```bash
# Gerar migration inicial
alembic revision --autogenerate -m "Initial migration with all tables"

# Aplicar migration (criar tabelas no Supabase)
alembic upgrade head
```

---

## 6. Verificar Tabelas no Supabase

1. No dashboard do Supabase, vá para **Table Editor**
2. Você deve ver as tabelas:
   - `users`
   - `provinces`
   - `municipalities`
   - `schools`
   - `markets`
   - `hospitals`
   - `alembic_version` (controle de migrations)

---

## 7. Migrar Dados JSON → PostgreSQL

Execute o script de migração:

```bash
python scripts/migrate_json_to_db.py
```

Este script irá:
1. Ler todos os dados JSON existentes
2. Inserir no PostgreSQL/Supabase
3. Preservar IDs e relacionamentos
4. Fazer backup dos arquivos JSON

---

## Informações Úteis

### Limites do Free Tier

- **Database**: 500 MB
- **Bandwidth**: 2 GB/mês
- **API Requests**: Ilimitado
- **Conexões**: 60 simultâneas

### URLs Importantes

- **Dashboard**: https://supabase.com/dashboard
- **API URL**: `https://xxx.supabase.co`
- **Database URL**: `postgresql://postgres:...@db.xxx.supabase.co:5432/postgres`
- **Documentação**: https://supabase.com/docs

### Segurança

⚠️ **NUNCA** commite o `.env` com a `DATABASE_URL` real!

O `.env.example` deve ter:
```bash
DATABASE_URL=postgresql://postgres:your-password@db.xxxxx.supabase.co:5432/postgres
```

---

## Troubleshooting

### Erro: "could not connect to server"
- Verifique se o projeto Supabase não está pausado
- Confira se a senha está correta
- Teste a conexão via browser no dashboard

### Erro: "password authentication failed"
- Senha incorreta no DATABASE_URL
- Resetar senha em Settings → Database → Reset database password

### Erro: "SSL connection required"
- Adicione `?sslmode=require` no final da URL:
  ```
  DATABASE_URL=postgresql://...postgres?sslmode=require
  ```

---

## Próximos Passos

Após configurar o Supabase:

1. ✅ DATABASE_URL configurada no .env
2. ✅ Testar conexão
3. ⏳ Executar migrations (criar tabelas)
4. ⏳ Migrar dados JSON → PostgreSQL
5. ⏳ Atualizar services para usar ORM
6. ⏳ Testar API com PostgreSQL
7. ⏳ Deploy na hospedagem (Railway/Render)

---

**Status Atual**: ⏳ Aguardando configuração do Supabase

Configure sua DATABASE_URL no `.env` para continuar!

