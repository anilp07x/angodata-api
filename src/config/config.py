"""
Configurações da aplicação AngoData API.
Define diferentes ambientes (desenvolvimento, produção) e suas respectivas configurações.
"""

import os


class Config:
    """Configuração base da aplicação."""
    
    # Configuração básica do Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # CORS
    CORS_HEADERS = 'Content-Type'
    
    # JSON
    JSON_AS_ASCII = False  # Permite caracteres portugueses nos JSON
    JSONIFY_PRETTYPRINT_REGULAR = True  # JSON formatado
    
    # Futuro: Configurações de banco de dados
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Configuração para ambiente de desenvolvimento."""
    
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuração para ambiente de produção."""
    
    DEBUG = False
    TESTING = False
    
    # Em produção, a SECRET_KEY deve vir de variável de ambiente
    SECRET_KEY = os.environ.get('SECRET_KEY')


# Mapeamento de configurações por ambiente
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
