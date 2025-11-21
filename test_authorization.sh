#!/bin/bash

echo "=== TESTE DE AUTORIZAÇÃO - FASE 3 ==="
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Base URL
BASE_URL="http://localhost:5001"

echo -e "${YELLOW}1. Testando GET público (sem autenticação)${NC}"
RESULT=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/provinces/all)
if [ "$RESULT" == "200" ]; then
    echo -e "${GREEN}✅ GET /provinces/all funcionou sem token (200)${NC}"
else
    echo -e "${RED}❌ GET /provinces/all falhou ($RESULT)${NC}"
fi
echo ""

echo -e "${YELLOW}2. Testando POST sem autenticação (deve falhar)${NC}"
RESULT=$(curl -s -X POST $BASE_URL/provinces \
  -H "Content-Type: application/json" \
  -d '{"nome":"Test","capital":"Test","area_km2":1000,"populacao":1000}')
if echo "$RESULT" | grep -q "Token de autenticação não fornecido"; then
    echo -e "${GREEN}✅ POST sem token foi bloqueado (401)${NC}"
else
    echo -e "${RED}❌ POST sem token não foi bloqueado${NC}"
fi
echo ""

echo -e "${YELLOW}3. Fazendo login como ADMIN${NC}"
ADMIN_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"anilpedro07@gmail.com","password":"password"}')
ADMIN_TOKEN=$(echo $ADMIN_LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)
if [ ! -z "$ADMIN_TOKEN" ]; then
    echo -e "${GREEN}✅ Login admin bem-sucedido${NC}"
else
    echo -e "${RED}❌ Falha no login admin${NC}"
    exit 1
fi
echo ""

echo -e "${YELLOW}4. Testando POST com token ADMIN${NC}"
RESULT=$(curl -s -X POST $BASE_URL/provinces \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"nome":"Província Admin","capital":"Capital Admin","area_km2":2000,"populacao":10000}')
if echo "$RESULT" | grep -q "sucesso"; then
    echo -e "${GREEN}✅ Admin conseguiu criar província${NC}"
    echo "$RESULT" | python3 -m json.tool 2>/dev/null | head -10
else
    echo -e "${RED}❌ Admin não conseguiu criar província${NC}"
    echo "$RESULT"
fi
echo ""

echo -e "${YELLOW}5. Fazendo login como EDITOR${NC}"
EDITOR_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"joao@example.com","password":"teste12345"}')
EDITOR_TOKEN=$(echo $EDITOR_LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)
if [ ! -z "$EDITOR_TOKEN" ]; then
    echo -e "${GREEN}✅ Login editor bem-sucedido${NC}"
else
    echo -e "${RED}❌ Falha no login editor${NC}"
fi
echo ""

echo -e "${YELLOW}6. Testando POST com token EDITOR${NC}"
RESULT=$(curl -s -X POST $BASE_URL/schools \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $EDITOR_TOKEN" \
  -d '{"nome":"Escola Editor","tipo":"Pública","endereco":"Rua Editor","provincia_id":1,"municipio_id":1}')
if echo "$RESULT" | grep -q "sucesso"; then
    echo -e "${GREEN}✅ Editor conseguiu criar escola${NC}"
    echo "$RESULT" | python3 -m json.tool 2>/dev/null | head -10
else
    echo -e "${RED}❌ Editor não conseguiu criar escola${NC}"
    echo "$RESULT"
fi
echo ""

echo -e "${YELLOW}7. Testando DELETE com token EDITOR${NC}"
RESULT=$(curl -s -X DELETE $BASE_URL/provinces/22 \
  -H "Authorization: Bearer $EDITOR_TOKEN")
if echo "$RESULT" | grep -q "sucesso"; then
    echo -e "${GREEN}✅ Editor conseguiu deletar província${NC}"
else
    echo -e "${RED}❌ Editor não conseguiu deletar${NC}"
    echo "$RESULT"
fi
echo ""

echo -e "${YELLOW}8. Registrando usuário comum (USER)${NC}"
USER_REG=$(curl -s -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"User Test","email":"user@example.com","password":"userpass123","role":"user"}')
if echo "$USER_REG" | grep -q "sucesso"; then
    echo -e "${GREEN}✅ Usuário comum registrado${NC}"
else
    echo -e "${YELLOW}⚠️  Usuário pode já existir${NC}"
fi
echo ""

echo -e "${YELLOW}9. Fazendo login como USER${NC}"
USER_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"userpass123"}')
USER_TOKEN=$(echo $USER_LOGIN | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)
if [ ! -z "$USER_TOKEN" ]; then
    echo -e "${GREEN}✅ Login user bem-sucedido${NC}"
else
    echo -e "${RED}❌ Falha no login user${NC}"
fi
echo ""

echo -e "${YELLOW}10. Testando POST com token USER (deve falhar)${NC}"
RESULT=$(curl -s -X POST $BASE_URL/provinces \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -d '{"nome":"Test User","capital":"Test","area_km2":1000,"populacao":1000}')
if echo "$RESULT" | grep -q "Permissões insuficientes\|Acesso negado"; then
    echo -e "${GREEN}✅ User foi bloqueado ao tentar criar província (403)${NC}"
else
    echo -e "${RED}❌ User não foi bloqueado!${NC}"
    echo "$RESULT"
fi
echo ""

echo "=== FIM DOS TESTES ==="
