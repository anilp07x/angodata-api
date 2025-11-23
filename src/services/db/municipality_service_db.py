"""
Municipality service using SQLAlchemy ORM.
Provides database-backed operations for municipalities.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.database.base import get_db_session
from src.database.models import Municipality, School, Market, Hospital


class MunicipalityServiceDB:
    """Service for managing municipalities with PostgreSQL database."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        Get all municipalities from database.
        
        Returns:
            List[Dict]: List of all municipalities with their data
        """
        try:
            with get_db_session() as session:
                municipalities = session.query(Municipality).order_by(
                    Municipality.nome
                ).all()
                return [municipality.to_dict() for municipality in municipalities]
        except SQLAlchemyError as e:
            print(f"Database error getting all municipalities: {e}")
            return []

    @staticmethod
    def get_by_id(municipality_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific municipality by ID.
        
        Args:
            municipality_id: The ID of the municipality to retrieve
            
        Returns:
            Dict or None: Municipality data if found, None otherwise
        """
        try:
            with get_db_session() as session:
                municipality = session.query(Municipality).filter(
                    Municipality.id == municipality_id
                ).first()
                return municipality.to_dict() if municipality else None
        except SQLAlchemyError as e:
            print(f"Database error getting municipality {municipality_id}: {e}")
            return None

    @staticmethod
    def get_by_province(province_id: int) -> List[Dict[str, Any]]:
        """
        Get all municipalities for a specific province.
        
        Args:
            province_id: ID of the province
            
        Returns:
            List[Dict]: List of municipalities in the province
        """
        try:
            with get_db_session() as session:
                municipalities = session.query(Municipality).filter(
                    Municipality.provincia_id == province_id
                ).order_by(Municipality.nome).all()
                return [municipality.to_dict() for municipality in municipalities]
        except SQLAlchemyError as e:
            print(f"Database error getting municipalities for province {province_id}: {e}")
            return []

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new municipality.
        
        Args:
            data: Municipality data (nome, provincia_id, area_km2, populacao)
            
        Returns:
            Dict or None: Created municipality data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                municipality = Municipality(
                    nome=data['nome'],
                    provincia_id=data['provincia_id'],
                    area_km2=data.get('area_km2'),
                    populacao=data.get('populacao')
                )
                session.add(municipality)
                session.flush()
                result = municipality.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error creating municipality: {e}")
            return None

    @staticmethod
    def update(municipality_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing municipality.
        
        Args:
            municipality_id: ID of the municipality to update
            data: Updated municipality data
            
        Returns:
            Dict or None: Updated municipality data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                municipality = session.query(Municipality).filter(
                    Municipality.id == municipality_id
                ).first()
                
                if not municipality:
                    return None
                
                # Update fields if provided
                if 'nome' in data:
                    municipality.nome = data['nome']
                if 'provincia_id' in data:
                    municipality.provincia_id = data['provincia_id']
                if 'area_km2' in data:
                    municipality.area_km2 = data['area_km2']
                if 'populacao' in data:
                    municipality.populacao = data['populacao']
                
                session.flush()
                result = municipality.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error updating municipality {municipality_id}: {e}")
            return None

    @staticmethod
    def delete(municipality_id: int) -> bool:
        """
        Delete a municipality by ID.
        
        Args:
            municipality_id: ID of the municipality to delete
            
        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            with get_db_session() as session:
                municipality = session.query(Municipality).filter(
                    Municipality.id == municipality_id
                ).first()
                
                if not municipality:
                    return False
                
                session.delete(municipality)
                return True
        except SQLAlchemyError as e:
            print(f"Database error deleting municipality {municipality_id}: {e}")
            return False

    @staticmethod
    def count() -> int:
        """
        Get total count of municipalities.
        
        Returns:
            int: Total number of municipalities
        """
        try:
            with get_db_session() as session:
                return session.query(Municipality).count()
        except SQLAlchemyError as e:
            print(f"Database error counting municipalities: {e}")
            return 0

    @staticmethod
    def has_dependencies(municipality_id: int) -> Dict[str, int]:
        """
        Check if municipality has dependent entities (schools, markets, hospitals).
        
        Args:
            municipality_id: ID of the municipality
            
        Returns:
            Dict with counts of schools, markets, hospitals and total
        """
        try:
            with get_db_session() as session:
                # Get the municipality to check its nome
                municipality = session.query(Municipality).filter(
                    Municipality.id == municipality_id
                ).first()
                
                if not municipality:
                    return {'schools': 0, 'markets': 0, 'hospitals': 0, 'total': 0}
                
                # Count dependencies by municipio name
                schools_count = session.query(School).filter(
                    School.municipio == municipality.nome
                ).count()
                
                markets_count = session.query(Market).filter(
                    Market.municipio == municipality.nome
                ).count()
                
                hospitals_count = session.query(Hospital).filter(
                    Hospital.municipio == municipality.nome
                ).count()
                
                return {
                    'schools': schools_count,
                    'markets': markets_count,
                    'hospitals': hospitals_count,
                    'total': schools_count + markets_count + hospitals_count
                }
        except SQLAlchemyError as e:
            print(f"Database error checking dependencies for municipality {municipality_id}: {e}")
            return {'schools': 0, 'markets': 0, 'hospitals': 0, 'total': 0}
