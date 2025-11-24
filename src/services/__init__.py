"""
Pacote de serviços de negócio da AngoData API.
Exporta todos os serviços para uso nas rotas.
"""

from .hospital_service import HospitalService
from .market_service import MarketService
from .municipality_service import MunicipalityService
from .province_service import ProvinceService
from .school_service import SchoolService

__all__ = ["ProvinceService", "MunicipalityService", "SchoolService", "MarketService", "HospitalService"]
