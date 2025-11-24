#!/bin/bash
# Deploy Helper Script - AngoData API

set -e  # Exit on error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== AngoData API - Deploy Script ===${NC}"

# Verificar se está no diretório correto
if [ ! -f "app.py" ]; then
    echo -e "${RED}Erro: Execute este script no diretório raiz do projeto${NC}"
    exit 1
fi

# Função para mostrar uso
usage() {
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  start       - Inicia containers (docker-compose up -d)"
    echo "  stop        - Para containers (docker-compose down)"
    echo "  restart     - Reinicia containers"
    echo "  build       - Rebuilda imagens Docker"
    echo "  logs        - Mostra logs dos containers"
    echo "  test        - Executa testes"
    echo "  lint        - Executa linting"
    echo "  format      - Formata código (black + isort)"
    echo "  clean       - Remove containers, volumes e imagens"
    echo "  setup       - Setup inicial do ambiente"
    echo "  migrate     - Executa migrações de banco"
    echo "  shell       - Abre shell no container da API"
    echo ""
    exit 1
}

# Verificar comando
if [ $# -eq 0 ]; then
    usage
fi

COMMAND=$1

case $COMMAND in
    start)
        echo -e "${YELLOW}Iniciando containers...${NC}"
        docker-compose up -d
        echo -e "${GREEN}✓ Containers iniciados${NC}"
        echo ""
        docker-compose ps
        ;;
    
    stop)
        echo -e "${YELLOW}Parando containers...${NC}"
        docker-compose down
        echo -e "${GREEN}✓ Containers parados${NC}"
        ;;
    
    restart)
        echo -e "${YELLOW}Reiniciando containers...${NC}"
        docker-compose restart
        echo -e "${GREEN}✓ Containers reiniciados${NC}"
        ;;
    
    build)
        echo -e "${YELLOW}Rebuilding imagens...${NC}"
        docker-compose build --no-cache
        echo -e "${GREEN}✓ Build concluído${NC}"
        ;;
    
    logs)
        docker-compose logs -f --tail=100
        ;;
    
    test)
        echo -e "${YELLOW}Executando testes...${NC}"
        if [ -d "venv" ]; then
            source venv/bin/activate
        fi
        pytest tests/ -v --cov=src --cov-report=term-missing
        ;;
    
    lint)
        echo -e "${YELLOW}Executando linting...${NC}"
        if [ -d "venv" ]; then
            source venv/bin/activate
        fi
        
        echo "→ Black (formatação)..."
        black --check src/ tests/
        
        echo "→ isort (imports)..."
        isort --check-only src/ tests/
        
        echo "→ Flake8 (linting)..."
        flake8 src/ tests/
        
        echo "→ Bandit (segurança)..."
        bandit -r src/ -ll
        
        echo -e "${GREEN}✓ Linting concluído${NC}"
        ;;
    
    format)
        echo -e "${YELLOW}Formatando código...${NC}"
        if [ -d "venv" ]; then
            source venv/bin/activate
        fi
        
        echo "→ Black..."
        black src/ tests/
        
        echo "→ isort..."
        isort src/ tests/
        
        echo -e "${GREEN}✓ Código formatado${NC}"
        ;;
    
    clean)
        echo -e "${RED}Atenção: Isso removerá todos os containers, volumes e imagens!${NC}"
        read -p "Continuar? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Limpando ambiente...${NC}"
            docker-compose down -v --rmi all
            echo -e "${GREEN}✓ Ambiente limpo${NC}"
        else
            echo "Operação cancelada"
        fi
        ;;
    
    setup)
        echo -e "${YELLOW}Setup inicial do ambiente...${NC}"
        
        # Criar .env se não existir
        if [ ! -f ".env" ]; then
            echo "→ Criando .env..."
            cp .env.example .env
            echo -e "${YELLOW}  Atenção: Edite o arquivo .env com suas configurações${NC}"
        fi
        
        # Criar virtual environment
        if [ ! -d "venv" ]; then
            echo "→ Criando virtual environment..."
            python3 -m venv venv
        fi
        
        # Ativar venv e instalar dependências
        echo "→ Instalando dependências..."
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        
        # Criar diretórios necessários
        echo "→ Criando diretórios..."
        mkdir -p logs
        mkdir -p ssl
        
        echo -e "${GREEN}✓ Setup concluído${NC}"
        echo ""
        echo "Próximos passos:"
        echo "1. Edite o arquivo .env com suas configurações"
        echo "2. Execute: source venv/bin/activate"
        echo "3. Execute: python app.py"
        ;;
    
    migrate)
        echo -e "${YELLOW}Executando migrações...${NC}"
        docker-compose exec api alembic upgrade head
        echo -e "${GREEN}✓ Migrações executadas${NC}"
        ;;
    
    shell)
        echo -e "${YELLOW}Abrindo shell no container da API...${NC}"
        docker-compose exec api /bin/bash
        ;;
    
    *)
        echo -e "${RED}Comando inválido: $COMMAND${NC}"
        usage
        ;;
esac
