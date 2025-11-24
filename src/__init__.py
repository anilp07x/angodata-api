"""
Pacote principal da AngoData API.
Contém a função factory para criar e configurar a aplicação Flask.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from src.config.config import config_by_name
from src.utils.security import add_security_headers
from src.utils.cache import init_cache
from src.swagger import api, init_swagger


def create_app(config_name='development'):
    """
    Factory function para criar e configurar a aplicação Flask.
    
    Args:
        config_name (str): Nome do ambiente de configuração ('development', 'production')
        
    Returns:
        Flask: Instância configurada da aplicação Flask
    """
    # Criar instância do Flask
    app = Flask(__name__)
    
    # Carregar configurações baseadas no ambiente
    app.config.from_object(config_by_name[config_name])
    
    # Inicializar database se USE_DATABASE=True
    init_database_if_enabled(app)
    
    # Carregar dados persistidos (se existirem e USE_DATABASE=False)
    load_persisted_data()
    
    # Habilitar CORS (Cross-Origin Resource Sharing)
    # Permite que a API seja acessada de diferentes domínios
    CORS(app)
    
    # Configurar Rate Limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )
    app.limiter = limiter
    
    # Configurar JWT
    jwt = JWTManager(app)
    configure_jwt_handlers(jwt)
    
    # Inicializar Cache (Redis ou Memory)
    init_cache(app)
    
    # Inicializar Swagger/OpenAPI
    init_swagger(app)
    
    # Adicionar security headers a todas as respostas
    app.after_request(add_security_headers)
    
    # Registrar Blueprints (rotas modulares)
    register_blueprints(app)
    
    # Registrar rota principal
    register_home_route(app)
    
    # Registrar manipuladores de erros
    register_error_handlers(app)
    
    return app


def init_database_if_enabled(app):
    """
    Inicializa conexão com banco de dados PostgreSQL se USE_DATABASE=True.
    
    Args:
        app (Flask): Instância da aplicação Flask
    """
    import os
    
    # Verificar se deve usar banco de dados
    use_database = os.getenv('USE_DATABASE', 'False').lower() == 'true'
    
    if use_database:
        from src.database.base import init_database, close_database
        
        # Inicializar conexão com database
        init_database()
        print("✓ Database PostgreSQL inicializado com sucesso")
        
        # Registrar cleanup ao desligar app
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            close_database()


def load_persisted_data():
    """
    Carrega dados persistidos de arquivos JSON.
    Se os arquivos não existirem, usa os dados hardcoded dos models.
    Somente carrega se USE_DATABASE=False.
    """
    import os
    
    # Não carregar JSON se estiver usando database
    use_database = os.getenv('USE_DATABASE', 'False').lower() == 'true'
    if use_database:
        print("✓ Usando PostgreSQL Database - dados JSON ignorados")
        return
    
    from src.database.json_storage import JSONStorage
    from src.models import province, municipality, school, market, hospital, user
    
    # Tentar carregar dados salvos
    persisted = JSONStorage.load_all_entities()
    
    # Se houver dados salvos, sobrescrever os models
    if persisted['provinces']:
        province.PROVINCES.clear()
        province.PROVINCES.extend(persisted['provinces'])
    
    if persisted['municipalities']:
        municipality.MUNICIPALITIES.clear()
        municipality.MUNICIPALITIES.extend(persisted['municipalities'])
    
    if persisted['schools']:
        school.SCHOOLS.clear()
        school.SCHOOLS.extend(persisted['schools'])
    
    if persisted['markets']:
        market.MARKETS.clear()
        market.MARKETS.extend(persisted['markets'])
    
    if persisted['hospitals']:
        hospital.HOSPITALS.clear()
        hospital.HOSPITALS.extend(persisted['hospitals'])
    
    if persisted.get('users'):
        user.USERS.clear()
        user.USERS.extend(persisted['users'])


def register_blueprints(app):
    """
    Registra todos os Blueprints (módulos de rotas) na aplicação.
    
    Args:
        app (Flask): Instância da aplicação Flask
    """
    from src.routes import (
        provinces_bp,
        municipalities_bp,
        schools_bp,
        markets_bp,
        hospitals_bp,
        auth_bp
    )
    
    # Registrar cada Blueprint
    app.register_blueprint(provinces_bp)
    app.register_blueprint(municipalities_bp)
    app.register_blueprint(schools_bp)
    app.register_blueprint(markets_bp)
    app.register_blueprint(hospitals_bp)
    app.register_blueprint(auth_bp)


def register_home_route(app):
    """
    Registra a rota principal (home) da API.
    
    Args:
        app (Flask): Instância da aplicação Flask
    """
    @app.route('/')
    def home():
        """
        GET /
        Endpoint principal que retorna informações sobre a API.
        """
        return jsonify({
            "message": "AngoData API a funcionar!",
            "version": "1.0.0",
            "endpoints": {
                "provinces": "/provinces/all, /provinces/<id>",
                "municipalities": "/municipalities/all, /municipalities/<id>",
                "schools": "/schools/all, /schools/<id>",
                "markets": "/markets/all, /markets/<id>",
                "hospitals": "/hospitals/all, /hospitals/<id>",
                "auth": "/auth/register, /auth/login, /auth/refresh, /auth/me, /auth/users"
            }
        }), 200


def configure_jwt_handlers(jwt):
    """
    Configura manipuladores de erros JWT personalizados.
    
    Args:
        jwt (JWTManager): Instância do JWTManager
    """
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """Manipulador para token expirado."""
        return jsonify({
            "success": False,
            "message": "O token de autenticação expirou. Por favor, faça login novamente."
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Manipulador para token inválido."""
        return jsonify({
            "success": False,
            "message": "Token de autenticação inválido. Por favor, forneça um token válido."
        }), 422
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        """Manipulador para requisição sem token."""
        return jsonify({
            "success": False,
            "message": "Token de autenticação não fornecido. Por favor, faça login."
        }), 401
    
    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header, jwt_payload):
        """Manipulador para quando um token fresh é necessário."""
        return jsonify({
            "success": False,
            "message": "Um token de autenticação recente é necessário. Por favor, faça login novamente."
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Manipulador para token revogado."""
        return jsonify({
            "success": False,
            "message": "O token de autenticação foi revogado. Por favor, faça login novamente."
        }), 401


def register_error_handlers(app):
    """
    Registra manipuladores de erros personalizados.
    
    Args:
        app (Flask): Instância da aplicação Flask
    """
    @app.errorhandler(404)
    def not_found(error):
        """Manipulador para erro 404 (Não Encontrado)."""
        return jsonify({
            "success": False,
            "error": "Endpoint não encontrado"
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Manipulador para erro 500 (Erro Interno do Servidor)."""
        return jsonify({
            "success": False,
            "error": "Erro interno do servidor"
        }), 500
