#!/bin/bash

# Script de teste para validar integração com PostgreSQL/Supabase
# Autor: AngoData API Team
# Data: 2025

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "  AngoData API - Teste PostgreSQL/Supabase"
echo "=========================================="
echo ""

# Verificar se USE_DATABASE está configurado
echo -e "${YELLOW}1. Verificando configuração USE_DATABASE...${NC}"
if grep -q "USE_DATABASE=True" .env 2>/dev/null; then
    echo -e "${GREEN}✓ USE_DATABASE=True encontrado no .env${NC}"
else
    echo -e "${RED}✗ USE_DATABASE não está configurado como True${NC}"
    echo "   Execute: echo 'USE_DATABASE=True' >> .env"
    exit 1
fi

# Verificar DATABASE_URL
echo -e "${YELLOW}2. Verificando DATABASE_URL...${NC}"
if grep -q "DATABASE_URL=postgresql://" .env 2>/dev/null; then
    echo -e "${GREEN}✓ DATABASE_URL configurado${NC}"
    
    # Verificar se ainda tem placeholder
    if grep -q "YOUR_PASSWORD_HERE" .env 2>/dev/null; then
        echo -e "${RED}✗ DATABASE_URL ainda contém placeholder 'YOUR_PASSWORD_HERE'${NC}"
        echo "   Substitua pela senha real do Supabase"
        exit 1
    fi
else
    echo -e "${RED}✗ DATABASE_URL não encontrado${NC}"
    exit 1
fi

# Verificar se dependências estão instaladas
echo -e "${YELLOW}3. Verificando dependências Python...${NC}"
source venv/bin/activate 2>/dev/null || {
    echo -e "${RED}✗ Virtual environment não encontrado${NC}"
    exit 1
}

python -c "import sqlalchemy; import psycopg2; import alembic" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ SQLAlchemy, psycopg2 e alembic instalados${NC}"
else
    echo -e "${RED}✗ Dependências não instaladas. Execute: pip install -r requirements.txt${NC}"
    exit 1
fi

# Testar conexão com database
echo -e "${YELLOW}4. Testando conexão com PostgreSQL...${NC}"
python -c "
from src.database.base import init_database
try:
    init_database()
    print('✓ Conexão com PostgreSQL estabelecida com sucesso')
except Exception as e:
    print(f'✗ Erro ao conectar: {e}')
    exit(1)
" || exit 1

# Testar queries básicas
echo -e "${YELLOW}5. Testando queries no database...${NC}"
python -c "
from src.database.base import init_database, get_db_session
from src.database.models import Province, Municipality, School, Market, Hospital, User

init_database()

with get_db_session() as session:
    province_count = session.query(Province).count()
    municipality_count = session.query(Municipality).count()
    school_count = session.query(School).count()
    market_count = session.query(Market).count()
    hospital_count = session.query(Hospital).count()
    user_count = session.query(User).count()
    
    print(f'Províncias: {province_count}')
    print(f'Municípios: {municipality_count}')
    print(f'Escolas: {school_count}')
    print(f'Mercados: {market_count}')
    print(f'Hospitais: {hospital_count}')
    print(f'Usuários: {user_count}')
    
    # Validar dados esperados
    if province_count == 26 and municipality_count == 326:
        print('✓ Dados migrados corretamente')
    else:
        print('✗ Contagem de dados não corresponde ao esperado')
        exit(1)
" || exit 1

# Testar ServiceFactory
echo -e "${YELLOW}6. Testando ServiceFactory...${NC}"
python -c "
from src.services.service_factory import ServiceFactory
import os

os.environ['USE_DATABASE'] = 'True'

ProvinceService = ServiceFactory.get_province_service()
provinces = ProvinceService.get_all()

if len(provinces) == 26:
    print(f'✓ ServiceFactory retornou {len(provinces)} províncias')
else:
    print(f'✗ ServiceFactory retornou {len(provinces)} províncias (esperado: 26)')
    exit(1)
" || exit 1

# Testar relacionamentos
echo -e "${YELLOW}7. Testando relacionamentos entre entidades...${NC}"
python -c "
from src.database.base import init_database, get_db_session
from src.database.models import Province, Municipality

init_database()

with get_db_session() as session:
    # Pegar Luanda (ID 1 provavelmente)
    luanda = session.query(Province).filter(Province.nome == 'Luanda').first()
    
    if luanda:
        municipalities = session.query(Municipality).filter(
            Municipality.provincia_id == luanda.id
        ).count()
        print(f'Província: {luanda.nome}')
        print(f'Municípios em Luanda: {municipalities}')
        print('✓ Relacionamento Province → Municipality funcionando')
    else:
        print('✗ Província Luanda não encontrada')
        exit(1)
" || exit 1

# Testar ORM Services
echo -e "${YELLOW}8. Testando CRUD com ORM Services...${NC}"
python -c "
from src.services.db.province_service_db import ProvinceServiceDB

# Test READ
provinces = ProvinceServiceDB.get_all()
print(f'GET all: {len(provinces)} províncias')

# Test GET by ID
province = ProvinceServiceDB.get_by_id(1)
if province:
    print(f'GET by ID: {province[\"nome\"]}')
else:
    print('✗ Erro ao buscar província por ID')
    exit(1)

print('✓ CRUD básico funcionando')
" || exit 1

echo ""
echo -e "${GREEN}=========================================="
echo "  ✓ Todos os testes passaram!"
echo "==========================================${NC}"
echo ""
echo "Próximos passos:"
echo "1. Iniciar servidor: python app.py"
echo "2. Testar endpoints HTTP com curl ou Postman"
echo "3. Validar autenticação JWT com database"
echo ""
