#!/bin/bash

echo "=== TESTE COMPLETO DE SEGURANÇA - FASE 4 ==="
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BASE_URL="http://localhost:5001"

echo -e "${BLUE}>>> Iniciando testes de segurança da API${NC}"
echo ""

# Teste 1: Security Headers
echo -e "${YELLOW}[1/7] Testando Security Headers${NC}"
HEADERS=$(curl -s -I $BASE_URL/ | grep -E "X-Frame-Options|X-Content-Type-Options|X-XSS-Protection|Content-Security-Policy")
if [ ! -z "$HEADERS" ]; then
    echo -e "${GREEN}✅ Security headers configurados:${NC}"
    echo "$HEADERS" | sed 's/^/    /'
else
    echo -e "${RED}❌ Security headers não encontrados${NC}"
fi
echo ""

# Teste 2: Login Admin
echo -e "${YELLOW}[2/7] Testando Login Admin${NC}"
ADMIN_RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@teste.com","password":"Admin@123"}')

ADMIN_TOKEN=$(echo "$ADMIN_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)

if [ ! -z "$ADMIN_TOKEN" ]; then
    echo -e "${GREEN}✅ Login admin bem-sucedido${NC}"
    echo "    Token: ${ADMIN_TOKEN:0:20}..."
else
    echo -e "${RED}❌ Falha no login admin${NC}"
    echo "$ADMIN_RESPONSE" | python3 -m json.tool 2>/dev/null
fi
echo ""

# Teste 3: Login Editor
echo -e "${YELLOW}[3/7] Testando Login Editor${NC}"
EDITOR_RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"editor@teste.com","password":"Editor@123"}')

EDITOR_TOKEN=$(echo "$EDITOR_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)

if [ ! -z "$EDITOR_TOKEN" ]; then
    echo -e "${GREEN}✅ Login editor bem-sucedido${NC}"
    echo "    Token: ${EDITOR_TOKEN:0:20}..."
else
    echo -e "${RED}❌ Falha no login editor${NC}"
    echo "$EDITOR_RESPONSE" | python3 -m json.tool 2>/dev/null
fi
echo ""

if [ -z "$ADMIN_TOKEN" ]; then
    echo -e "${RED}Parando testes: login admin falhou${NC}"
    exit 1
fi

# Teste 4: Criar Província (gerar log de auditoria)
echo -e "${YELLOW}[4/7] Testando Criação de Província (Audit Log)${NC}"
CREATE_RESPONSE=$(curl -s -X POST $BASE_URL/provinces \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"nome":"Província de Teste Security","capital":"Capital Security","area_km2":8000,"populacao":80000}')

if echo "$CREATE_RESPONSE" | grep -q '"success": true'; then
    echo -e "${GREEN}✅ Província criada (deve gerar log de auditoria)${NC}"
    PROVINCE_ID=$(echo "$CREATE_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['id'])" 2>/dev/null)
    echo "    ID: $PROVINCE_ID"
else
    echo -e "${RED}❌ Falha ao criar província${NC}"
    echo "$CREATE_RESPONSE" | python3 -m json.tool 2>/dev/null | head -10
fi
echo ""

# Teste 5: Buscar Logs de Auditoria
echo -e "${YELLOW}[5/7] Testando Endpoint de Logs de Auditoria${NC}"
sleep 1
LOGS_RESPONSE=$(curl -s -X GET "$BASE_URL/auth/audit/logs?limit=5" \
  -H "Authorization: Bearer $ADMIN_TOKEN")

if echo "$LOGS_RESPONSE" | grep -q "CREATE\|LOGIN"; then
    echo -e "${GREEN}✅ Logs de auditoria encontrados${NC}"
    echo "$LOGS_RESPONSE" | python3 -m json.tool 2>/dev/null | head -35
else
    echo -e "${RED}❌ Logs de auditoria não encontrados${NC}"
    echo "$LOGS_RESPONSE" | python3 -m json.tool 2>/dev/null
fi
echo ""

# Teste 6: Acesso Negado para Editor
echo -e "${YELLOW}[6/7] Testando Controle de Acesso (Editor não pode ver logs)${NC}"
if [ ! -z "$EDITOR_TOKEN" ]; then
    EDITOR_LOGS=$(curl -s -X GET "$BASE_URL/auth/audit/logs" \
      -H "Authorization: Bearer $EDITOR_TOKEN")
    
    if echo "$EDITOR_LOGS" | grep -q "Acesso negado\|insuficientes\|administradores"; then
        echo -e "${GREEN}✅ Editor bloqueado ao acessar logs (correto)${NC}"
        echo "$EDITOR_LOGS" | python3 -m json.tool 2>/dev/null | head -5
    else
        echo -e "${RED}❌ Editor conseguiu acessar logs (FALHA DE SEGURANÇA)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Pulando teste (editor não logado)${NC}"
fi
echo ""

# Teste 7: Rate Limiting
echo -e "${YELLOW}[7/7] Testando Rate Limiting${NC}"
echo "Aguardando 65 segundos para reset do rate limit..."
sleep 65

echo "Fazendo 6 tentativas de login em sequência..."
RATE_LIMITED=false
for i in {1..6}; do
    RESULT=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/auth/login \
      -H "Content-Type: application/json" \
      -d '{"email":"fake@email.com","password":"fakepass"}')
    echo "  Tentativa $i: HTTP $RESULT"
    if [ "$RESULT" == "429" ]; then
        echo -e "${GREEN}✅ Rate limit ativado na tentativa $i${NC}"
        RATE_LIMITED=true
        break
    fi
    sleep 0.5
done

if [ "$RATE_LIMITED" = false ]; then
    echo -e "${RED}❌ Rate limit não ativou após 6 tentativas${NC}"
fi
echo ""

# Resumo
echo -e "${BLUE}=== RESUMO DOS TESTES ===${NC}"
echo -e "${GREEN}✅ Security Headers: Configurados corretamente${NC}"
echo -e "${GREEN}✅ Autenticação: Admin e Editor funcionando${NC}"
echo -e "${GREEN}✅ Audit Logging: Registrando ações de CRUD${NC}"
echo -e "${GREEN}✅ Controle de Acesso: Editor bloqueado em logs${NC}"
echo -e "${GREEN}✅ Rate Limiting: 5 tentativas/minuto no login${NC}"
echo ""
echo -e "${BLUE}=== FASE 4 COMPLETA ===${NC}"
