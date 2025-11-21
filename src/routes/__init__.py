"""
Pacote de rotas da AngoData API.
Exporta todos os Blueprints para registro na aplicação.
"""

from .provinces import provinces_bp
from .municipalities import municipalities_bp
from .schools import schools_bp
from .markets import markets_bp
from .hospitals import hospitals_bp

__all__ = [
    'provinces_bp',
    'municipalities_bp',
    'schools_bp',
    'markets_bp',
    'hospitals_bp'
]
