"""
Pacote principal da AngoData API.
Contém a função factory para criar e configurar a aplicação Flask.
"""

from flask import Flask, jsonify
from flask_cors import CORS
from src.config.config import config_by_name


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
    
    # Habilitar CORS (Cross-Origin Resource Sharing)
    # Permite que a API seja acessada de diferentes domínios
    CORS(app)
    
    # Registrar Blueprints (rotas modulares)
    register_blueprints(app)
    
    # Registrar rota principal
    register_home_route(app)
    
    # Registrar manipuladores de erros
    register_error_handlers(app)
    
    return app


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
        hospitals_bp
    )
    
    # Registrar cada Blueprint
    app.register_blueprint(provinces_bp)
    app.register_blueprint(municipalities_bp)
    app.register_blueprint(schools_bp)
    app.register_blueprint(markets_bp)
    app.register_blueprint(hospitals_bp)


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
                "hospitals": "/hospitals/all, /hospitals/<id>"
            }
        }), 200


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
