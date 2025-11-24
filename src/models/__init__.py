"""
Pacote de modelos de dados da AngoData API.
Exporta todos os modelos de dados para uso na aplicação.
"""

from .hospital import HOSPITALS
from .market import MARKETS
from .municipality import MUNICIPALITIES
from .province import PROVINCES
from .school import SCHOOLS

__all__ = ["PROVINCES", "MUNICIPALITIES", "SCHOOLS", "MARKETS", "HOSPITALS"]
