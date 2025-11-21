# AngoData API - AI Coding Agent Instructions

## Project Overview
REST API em Flask que fornece dados públicos de Angola (províncias, municípios, escolas, mercados e hospitais). Arquitetura modular e escalável usando padrão Factory, Blueprints e separação de responsabilidades.

## Tech Stack
- **Python**: 3.12.3
- **Web Framework**: Flask 3.1.2
- **CORS**: Flask-CORS 5.0.0
- **Dados**: In-memory (futuro: SQLAlchemy + PostgreSQL)

## Project Structure
```
angodata-api/
├── app.py                      # Ponto de entrada da aplicação
├── requirements.txt            # Dependências Python
├── src/
│   ├── __init__.py            # Factory function create_app()
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py          # Configurações por ambiente
│   ├── models/                # Dados in-memory (structs)
│   │   ├── __init__.py
│   │   ├── province.py
│   │   ├── municipality.py
│   │   ├── school.py
│   │   ├── market.py
│   │   └── hospital.py
│   ├── services/              # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── province_service.py
│   │   ├── municipality_service.py
│   │   ├── school_service.py
│   │   ├── market_service.py
│   │   └── hospital_service.py
│   ├── routes/                # Blueprints (endpoints)
│   │   ├── __init__.py
│   │   ├── provinces.py
│   │   ├── municipalities.py
│   │   ├── schools.py
│   │   ├── markets.py
│   │   └── hospitals.py
│   └── database/              # Placeholder para futuro DB
│       └── __init__.py
└── venv/                      # Virtual environment
```

## Architecture Patterns

### Factory Pattern
A aplicação usa `create_app()` em `src/__init__.py` para inicialização modular:
- Permite diferentes configurações (development/production)
- Facilita testes unitários
- Registra Blueprints, CORS e error handlers centralizadamente

### Three-Layer Architecture
1. **Routes (Blueprints)**: Recebem requests HTTP, validam entrada
2. **Services**: Contêm lógica de negócio, manipulam dados
3. **Models**: Estruturas de dados (atualmente in-memory lists de dicts)

### Blueprint Organization
Cada entidade tem seu Blueprint com URL prefix:
- `/provinces/all` e `/provinces/<id>`
- `/municipalities/all` e `/municipalities/<id>`
- `/schools/all` e `/schools/<id>`
- `/markets/all` e `/markets/<id>`
- `/hospitals/all` e `/hospitals/<id>`

## Development Workflow

### Environment Setup
```bash
# Ativar virtual environment
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Running the Application
```bash
# Executar em modo development (debug=True)
python app.py

# API estará disponível em http://0.0.0.0:5000
```

### Testing Endpoints
```bash
# Home endpoint
curl http://localhost:5000/

# Listar todas as províncias
curl http://localhost:5000/provinces/all

# Buscar província específica
curl http://localhost:5000/provinces/1
```

## Code Conventions

### Language & Messages
- **Português**: Todos os responses da API, mensagens de erro e nomes de campos em português
- **Inglês**: Código, comentários técnicos, nomes de funções/classes

### Response Format
Todas as respostas seguem padrão consistente:
```python
# Sucesso
{
    "success": True,
    "total": 18,  # Para listagens
    "data": [...]
}

# Erro
{
    "success": False,
    "message": "Descrição do erro em português"
}
```

### Service Layer Pattern
Services usam métodos estáticos para operações de dados:
- `get_all()`: Retorna lista completa
- `get_by_id(id)`: Retorna item específico ou None
- `get_by_province(province_id)`: Filtra por província (onde aplicável)

### Import Organization
Imports absolutos a partir de `src/`:
```python
from src.models.province import PROVINCES
from src.services.province_service import ProvinceService
```

## Current Limitations & Future Roadmap

### Database Migration
- **Atual**: Dados in-memory em listas Python
- **Futuro**: Migrar para SQLAlchemy + PostgreSQL
- Estrutura preparada em `src/database/` para integração

### Planned Features
- Validação de dados com Marshmallow
- Autenticação JWT
- Paginação para endpoints `/all`
- Filtros e busca avançada
- Testes unitários e integração
- Variáveis de ambiente com python-dotenv
- Documentação OpenAPI/Swagger

## Important Notes
- CORS habilitado globalmente - restringir em produção
- Debug mode ativo - desabilitar para production
- Sem banco de dados - dados resetam ao reiniciar
- Sem autenticação - endpoints totalmente públicos
- JSON formatado com `JSON_AS_ASCII=False` para suportar acentuação portuguesa
