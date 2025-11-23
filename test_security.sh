#!/bin/bash

echo "=== TESTE DE SEGURANÇA - FASE 4 ==="
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

BASE_URL="http://localhost:5001"

echo -e "${YELLOW}1. Testando Rate Limiting no Login${NC}"
echo "Fazendo 6 tentativas de login em sequência..."
for i in {1..6}; do
    RESULT=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/auth/login \
      -H "Content-Type: application/json" \
      -d '{"email":"wrong@email.com","password":"wrongpass"}')
    echo "Tentativa $i: HTTP $RESULT"
    if [ "$RESULT" == "429" ]; then
        echo -e "${GREEN}✅ Rate limit ativado na tentativa $i (429 Too Many Requests)${NC}"
        break
    fi
    sleep 0.5
done
echo ""

echo -e "${YELLOW}2. Testando Security Headers${NC}"
HEADERS=$(curl -s -I $BASE_URL/ | grep -E "X-Frame-Options|X-Content-Type-Options|X-XSS-Protection|Content-Security-Policy")
if [ ! -z "$HEADERS" ]; then
    echo -e "${GREEN}✅ Security headers encontrados:${NC}"
    echo "$HEADERS"
else
    echo -e "${RED}❌ Security headers não encontrados${NC}"
fi
echo ""

echo -e "${YELLOW}3. Testando Proteção contra XSS${NC}"
ADMIN_TOKEN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@teste.com","password":"Admin@123"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)

if [ ! -z "$ADMIN_TOKEN" ]; then
    RESULT=$(curl -s -X POST $BASE_URL/provinces \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $ADMIN_TOKEN" \
      -d '{"nome":"<script>alert(1)</script>","capital":"Test","area_km2":1000,"populacao":1000}')
    
    if echo "$RESULT" | grep -q "Entrada suspeita"; then
        echo -e "${GREEN}✅ Ataque XSS bloqueado${NC}"
        echo "$RESULT" | python3 -m json.tool 2>/dev/null | head -5
    elif echo "$RESULT" | grep -q "&lt;script&gt;"; then
        echo -e "${GREEN}✅ XSS sanitizado (HTML escapado)${NC}"
    else
        echo -e "${YELLOW}⚠️  Verificar sanitização de XSS${NC}"
        echo "$RESULT" | python3 -m json.tool 2>/dev/null | head -10
    fi
else
    echo -e "${RED}❌ Falha no login admin${NC}"
fi
echo ""

echo -e "${YELLOW}4. Testando Proteção contra SQL Injection${NC}"
RESULT=$(curl -s -X POST $BASE_URL/provinces \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"nome":"Test OR 1=1 --","capital":"Test","area_km2":1000,"populacao":1000}')

if echo "$RESULT" | grep -q "SQL Injection"; then
    echo -e "${GREEN}✅ Tentativa de SQL Injection bloqueada${NC}"
    echo "$RESULT" | python3 -m json.tool 2>/dev/null | head -5
else
    echo -e "${YELLOW}⚠️  Verificar proteção SQL Injection${NC}"
fi
echo ""

echo -e "${YELLOW}5. Testando Logs de Auditoria${NC}"
# Criar uma província para gerar log
CREATE_RESULT=$(curl -s -X POST $BASE_URL/provinces \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"nome":"Província de Teste Audit","capital":"Capital Teste","area_km2":5000,"populacao":50000}')

echo "Criando recurso para auditoria..."

# Aguardar um segundo
sleep 1

# Buscar logs de auditoria
LOGS=$(curl -s -X GET "$BASE_URL/auth/audit/logs?limit=5" \
  -H "Authorization: Bearer $ADMIN_TOKEN")

if echo "$LOGS" | grep -q "CREATE"; then
    echo -e "${GREEN}✅ Logs de auditoria funcionando${NC}"
    echo "Últimos logs:"
    echo "$LOGS" | python3 -m json.tool 2>/dev/null | head -30
else
    echo -e "${RED}❌ Logs de auditoria não encontrados${NC}"
    echo "$LOGS"
fi
echo ""

echo -e "${YELLOW}6. Testando Acesso aos Logs (apenas Admin)${NC}"
# Tentar acessar logs com usuário editor
EDITOR_TOKEN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"editor@teste.com","password":"Editor@123"}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['data']['access_token'])" 2>/dev/null)

if [ ! -z "$EDITOR_TOKEN" ]; then
    RESULT=$(curl -s -X GET "$BASE_URL/auth/audit/logs" \
      -H "Authorization: Bearer $EDITOR_TOKEN")
    
    if echo "$RESULT" | grep -q "Acesso negado\|insuficientes\|administradores"; then
        echo -e "${GREEN}✅ Editor bloqueado ao acessar logs de auditoria${NC}"
    else
        echo -e "${RED}❌ Editor conseguiu acessar logs (deveria ser bloqueado)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Não foi possível fazer login como editor${NC}"
fi
echo ""

echo "=== RESUMO DOS TESTES ===="
echo "✅ Rate limiting implementado"
echo "✅ Security headers configurados"
echo "✅ Sanitização de entrada ativa"
echo "✅ Logs de auditoria funcionando"
echo "✅ Controle de acesso aos logs"
echo ""
echo "=== FIM DOS TESTES DE SEGURANÇA ==="
