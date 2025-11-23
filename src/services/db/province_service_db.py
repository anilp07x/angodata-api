"""
Province service using SQLAlchemy ORM.
Provides database-backed operations for provinces.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.database.base import get_db_session
from src.database.models import Province, Municipality


class ProvinceServiceDB:
    """Service for managing provinces with PostgreSQL database."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        Get all provinces from database.
        
        Returns:
            List[Dict]: List of all provinces with their data
        """
        try:
            with get_db_session() as session:
                provinces = session.query(Province).order_by(Province.nome).all()
                return [province.to_dict() for province in provinces]
        except SQLAlchemyError as e:
            print(f"Database error getting all provinces: {e}")
            return []

    @staticmethod
    def get_by_id(province_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific province by ID.
        
        Args:
            province_id: The ID of the province to retrieve
            
        Returns:
            Dict or None: Province data if found, None otherwise
        """
        try:
            with get_db_session() as session:
                province = session.query(Province).filter(
                    Province.id == province_id
                ).first()
                return province.to_dict() if province else None
        except SQLAlchemyError as e:
            print(f"Database error getting province {province_id}: {e}")
            return None

    @staticmethod
    def get_by_name(nome: str) -> Optional[Dict[str, Any]]:
        """
        Get a province by name (case-insensitive).
        
        Args:
            nome: Name of the province
            
        Returns:
            Dict or None: Province data if found, None otherwise
        """
        try:
            with get_db_session() as session:
                province = session.query(Province).filter(
                    Province.nome.ilike(nome)
                ).first()
                return province.to_dict() if province else None
        except SQLAlchemyError as e:
            print(f"Database error getting province by name '{nome}': {e}")
            return None

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new province.
        
        Args:
            data: Province data (nome, capital, area_km2, populacao)
            
        Returns:
            Dict or None: Created province data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                province = Province(
                    nome=data['nome'],
                    capital=data.get('capital'),
                    area_km2=data.get('area_km2'),
                    populacao=data.get('populacao')
                )
                session.add(province)
                session.flush()  # Get the ID before commit
                result = province.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error creating province: {e}")
            return None

    @staticmethod
    def update(province_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing province.
        
        Args:
            province_id: ID of the province to update
            data: Updated province data
            
        Returns:
            Dict or None: Updated province data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                province = session.query(Province).filter(
                    Province.id == province_id
                ).first()
                
                if not province:
                    return None
                
                # Update fields if provided
                if 'nome' in data:
                    province.nome = data['nome']
                if 'capital' in data:
                    province.capital = data['capital']
                if 'area_km2' in data:
                    province.area_km2 = data['area_km2']
                if 'populacao' in data:
                    province.populacao = data['populacao']
                
                session.flush()
                result = province.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error updating province {province_id}: {e}")
            return None

    @staticmethod
    def delete(province_id: int) -> bool:
        """
        Delete a province by ID.
        
        Args:
            province_id: ID of the province to delete
            
        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            with get_db_session() as session:
                province = session.query(Province).filter(
                    Province.id == province_id
                ).first()
                
                if not province:
                    return False
                
                session.delete(province)
                return True
        except SQLAlchemyError as e:
            print(f"Database error deleting province {province_id}: {e}")
            return False

    @staticmethod
    def count() -> int:
        """
        Get total count of provinces.
        
        Returns:
            int: Total number of provinces
        """
        try:
            with get_db_session() as session:
                return session.query(Province).count()
        except SQLAlchemyError as e:
            print(f"Database error counting provinces: {e}")
            return 0

    @staticmethod
    def has_municipalities(province_id: int) -> int:
        """
        Check how many municipalities belong to a province.
        
        Args:
            province_id: ID of the province
            
        Returns:
            int: Number of municipalities in the province
        """
        try:
            with get_db_session() as session:
                return session.query(Municipality).filter(
                    Municipality.provincia_id == province_id
                ).count()
        except SQLAlchemyError as e:
            print(f"Database error checking municipalities for province {province_id}: {e}")
            return 0
