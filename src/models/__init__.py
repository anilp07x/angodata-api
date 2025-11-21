"""
Pacote de modelos de dados da AngoData API.
Exporta todos os modelos de dados para uso na aplicação.
"""

from .province import PROVINCES
from .municipality import MUNICIPALITIES
from .school import SCHOOLS
from .market import MARKETS
from .hospital import HOSPITALS

__all__ = ['PROVINCES', 'MUNICIPALITIES', 'SCHOOLS', 'MARKETS', 'HOSPITALS']
