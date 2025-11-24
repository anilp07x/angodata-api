"""
Service Factory for switching between JSON and Database storage.

This factory provides a unified interface to access services,
allowing seamless transition from JSON to PostgreSQL database.
"""

import os
from typing import Any


class ServiceFactory:
    """
    Factory class to provide appropriate service implementation
    based on USE_DATABASE environment variable.
    """

    @staticmethod
    def _use_database() -> bool:
        """
        Check if database should be used.

        Returns:
            bool: True if USE_DATABASE=True, False otherwise
        """
        return os.getenv("USE_DATABASE", "False").lower() == "true"

    @staticmethod
    def get_province_service() -> Any:
        """
        Get Province service (DB or JSON).

        Returns:
            ProvinceService: Either ProvinceServiceDB or ProvinceService
        """
        if ServiceFactory._use_database():
            from src.services.db.province_service_db import ProvinceServiceDB

            return ProvinceServiceDB
        else:
            from src.services.province_service import ProvinceService

            return ProvinceService

    @staticmethod
    def get_municipality_service() -> Any:
        """
        Get Municipality service (DB or JSON).

        Returns:
            MunicipalityService: Either MunicipalityServiceDB or MunicipalityService
        """
        if ServiceFactory._use_database():
            from src.services.db.municipality_service_db import MunicipalityServiceDB

            return MunicipalityServiceDB
        else:
            from src.services.municipality_service import MunicipalityService

            return MunicipalityService

    @staticmethod
    def get_school_service() -> Any:
        """
        Get School service (DB or JSON).

        Returns:
            SchoolService: Either SchoolServiceDB or SchoolService
        """
        if ServiceFactory._use_database():
            from src.services.db.school_service_db import SchoolServiceDB

            return SchoolServiceDB
        else:
            from src.services.school_service import SchoolService

            return SchoolService

    @staticmethod
    def get_market_service() -> Any:
        """
        Get Market service (DB or JSON).

        Returns:
            MarketService: Either MarketServiceDB or MarketService
        """
        if ServiceFactory._use_database():
            from src.services.db.market_service_db import MarketServiceDB

            return MarketServiceDB
        else:
            from src.services.market_service import MarketService

            return MarketService

    @staticmethod
    def get_hospital_service() -> Any:
        """
        Get Hospital service (DB or JSON).

        Returns:
            HospitalService: Either HospitalServiceDB or HospitalService
        """
        if ServiceFactory._use_database():
            from src.services.db.hospital_service_db import HospitalServiceDB

            return HospitalServiceDB
        else:
            from src.services.hospital_service import HospitalService

            return HospitalService

    @staticmethod
    def get_user_service() -> Any:
        """
        Get User service (DB or JSON).

        Returns:
            UserService: Either UserServiceDB or UserService (from auth)
        """
        if ServiceFactory._use_database():
            from src.services.db.user_service_db import UserServiceDB

            return UserServiceDB
        else:
            from src.auth.user_service import UserService

            return UserService
