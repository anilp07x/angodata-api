"""
Pacote de serviços de negócio da AngoData API.
Exporta todos os serviços para uso nas rotas.
"""

from .province_service import ProvinceService
from .municipality_service import MunicipalityService
from .school_service import SchoolService
from .market_service import MarketService
from .hospital_service import HospitalService

__all__ = [
    'ProvinceService',
    'MunicipalityService',
    'SchoolService',
    'MarketService',
    'HospitalService'
]
