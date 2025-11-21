"""
Configurações da aplicação AngoData API.
Define diferentes ambientes (desenvolvimento, produção) e suas respectivas configurações.
"""

import os
from datetime import timedelta


class Config:
    """Configuração base da aplicação."""
    
    # Configuração básica do Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # CORS
    CORS_HEADERS = 'Content-Type'
    
    # JSON
    JSON_AS_ASCII = False  # Permite caracteres portugueses nos JSON
    JSONIFY_PRETTYPRINT_REGULAR = True  # JSON formatado
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400)))  # 24h default
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 2592000)))  # 30d default
    JWT_ALGORITHM = 'HS256'
    
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
