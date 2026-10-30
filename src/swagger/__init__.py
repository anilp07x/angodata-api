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
**REST API que fornece dados públicos de Angola.**

## Recursos Disponíveis

- **Províncias**: 21 províncias de Angola
- **Municípios**: 326 municípios
- **Escolas**: Instituições de ensino
- **Mercados**: Mercados públicos
- **Hospitais**: Unidades de saúde

## Autenticação

A API utiliza JWT (JSON Web Tokens). Para endpoints protegidos (🔒):

1. Faça `POST /auth/login` para obter o token
2. Clique no botão **Authorize** (ou o cadeado no endpoint) e cole o token
3. O header enviado será: `Authorization: Bearer <seu-token>`

## Rate Limiting

- **200 requisições por dia** (padrão, por IP)
- **50 requisições por hora**
- Login: **5 tentativas por minuto**
- Excedores retornam `429 Too Many Requests`

## Paginação

Endpoints de listagem suportam paginação:
- `page`: número da página (padrão: 1)
- `per_page`: itens por página (padrão: 20, máximo: 100)
- `sort_by`: campo para ordenação
- `order`: ordem (asc/desc)
- `search`: termo de busca

Exemplo: `/provinces/all?page=1&per_page=20&sort_by=nome&order=asc&search=Luanda`

## Modo de uso

- GETs públicos: livres, sem autenticação
- POST/PUT/DELETE: exigem **Authorize** com o token JWT
    """,
    doc=False,  # UI customizada em docs_ui.py (rota /docs) — desliga a UI vanilla do flask-restx
    authorizations={
        "Bearer": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Adicione o token JWT no formato: Bearer <token>",
        }
    },
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
    from flask import Response

    from src.swagger.docs_ui import get_docs_page

    @api_bp.route("/docs")
    def swagger_docs():
        """Página de documentação customizada (Swagger UI, tema Angola)."""
        return Response(
            get_docs_page(spec_url="/api/swagger.json"),
            mimetype="text/html; charset=utf-8",
            headers={"Cache-Control": "no-store"},
        )

    app.register_blueprint(api_bp, url_prefix="/api")
    print("✓ Swagger/OpenAPI inicializado em /api/docs")
