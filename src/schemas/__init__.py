"""
Schemas de validação usando Marshmallow
"""

from .province_schema import ProvinceSchema
from .municipality_schema import MunicipalitySchema
from .school_schema import SchoolSchema
from .market_schema import MarketSchema
from .hospital_schema import HospitalSchema

__all__ = [
    'ProvinceSchema',
    'MunicipalitySchema',
    'SchoolSchema',
    'MarketSchema',
    'HospitalSchema'
]
