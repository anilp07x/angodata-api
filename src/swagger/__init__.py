"""
Configuração Swagger/OpenAPI com flask-restx.
"""

from flask import Blueprint
from flask_restx import Api

# Criar blueprint para API (SEM url_prefix aqui)
api_bp = Blueprint("api", __name__)

# Configuração da API com metadados
api = Api(
    api_bp,
    version="1.0.0",
    title="AngoData API",
    description="""
REST API que fornece dados públicos de Angola.

## Recursos Disponíveis

- **Províncias**: 21 províncias de Angola
- **Municípios**: 326 municípios
- **Escolas**: Instituições de ensino
- **Mercados**: Mercados públicos
- **Hospitais**: Unidades de saúde

## Autenticação

A API utiliza JWT (JSON Web Tokens) para autenticação. Para acessar endpoints protegidos:

1. Obtenha um token através do endpoint `/auth/login`
2. Inclua o token no header: `Authorization: Bearer <seu-token>`

## Rate Limiting

- 100 requisições por minuto por IP
- Endpoints públicos: sem autenticação necessária
- Endpoints protegidos: requerem autenticação JWT

## Paginação

Endpoints de listagem suportam paginação:
- `page`: número da página (padrão: 1)
- `per_page`: itens por página (padrão: 20, máximo: 100)
- `sort_by`: campo para ordenação
- `order`: ordem (asc/desc)
- `search`: termo de busca

Exemplo: `/provinces/all?page=1&per_page=20&sort_by=nome&order=asc&search=Luanda`
    """,
    doc="/docs",
    authorizations={
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Adicione o token JWT no formato: Bearer <token>",
        }
    },
    security="Bearer",
    contact="Anilson Pedro",
    contact_email="anilpedro07x@outlook.com",
    license="MIT",
    ordered=True,
)

# Importar resources (para registrar os endpoints)
from src.swagger import (
    auth_resources,
    hospitals_resources,
    markets_resources,
    municipalities_resources,
    provinces_resources,
    schools_resources,
)

# Importar namespaces
from src.swagger.auth_ns import auth_ns
from src.swagger.hospitals_ns import hospitals_ns
from src.swagger.markets_ns import markets_ns
from src.swagger.municipalities_ns import municipalities_ns
from src.swagger.provinces_ns import provinces_ns
from src.swagger.schools_ns import schools_ns

# Registrar namespaces
api.add_namespace(auth_ns, path="/auth")
api.add_namespace(provinces_ns, path="/provinces")
api.add_namespace(municipalities_ns, path="/municipalities")
api.add_namespace(schools_ns, path="/schools")
api.add_namespace(markets_ns, path="/markets")
api.add_namespace(hospitals_ns, path="/hospitals")


def init_swagger(app):
    """
    Inicializa Swagger/OpenAPI na aplicação.

    Args:
        app: Instância Flask
    """
    app.register_blueprint(api_bp, url_prefix="/api")
    print("✓ Swagger/OpenAPI inicializado em /api/docs")
