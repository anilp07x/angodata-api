"""
Schemas de validação usando Marshmallow
"""

from .hospital_schema import HospitalSchema
from .market_schema import MarketSchema
from .municipality_schema import MunicipalitySchema
from .province_schema import ProvinceSchema
from .school_schema import SchoolSchema

__all__ = ["ProvinceSchema", "MunicipalitySchema", "SchoolSchema", "MarketSchema", "HospitalSchema"]
