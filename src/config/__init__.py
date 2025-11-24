"""
Pacote de configuração da AngoData API.
Exporta as classes de configuração para uso na aplicação.
"""

from .config import Config, DevelopmentConfig, ProductionConfig

__all__ = ["Config", "DevelopmentConfig", "ProductionConfig"]
