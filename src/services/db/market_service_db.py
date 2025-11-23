"""
Market service using SQLAlchemy ORM.
Provides database-backed operations for markets.
"""

from typing import Optional, List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError

from src.database.base import get_db_session
from src.database.models import Market


class MarketServiceDB:
    """Service for managing markets with PostgreSQL database."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """
        Get all markets from database.
        
        Returns:
            List[Dict]: List of all markets with their data
        """
        try:
            with get_db_session() as session:
                markets = session.query(Market).order_by(Market.nome).all()
                return [market.to_dict() for market in markets]
        except SQLAlchemyError as e:
            print(f"Database error getting all markets: {e}")
            return []

    @staticmethod
    def get_by_id(market_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific market by ID.
        
        Args:
            market_id: The ID of the market to retrieve
            
        Returns:
            Dict or None: Market data if found, None otherwise
        """
        try:
            with get_db_session() as session:
                market = session.query(Market).filter(
                    Market.id == market_id
                ).first()
                return market.to_dict() if market else None
        except SQLAlchemyError as e:
            print(f"Database error getting market {market_id}: {e}")
            return None

    @staticmethod
    def get_by_province(province_id: int) -> List[Dict[str, Any]]:
        """
        Get all markets for a specific province.
        
        Args:
            province_id: ID of the province
            
        Returns:
            List[Dict]: List of markets in the province
        """
        try:
            with get_db_session() as session:
                markets = session.query(Market).filter(
                    Market.provincia_id == province_id
                ).order_by(Market.nome).all()
                return [market.to_dict() for market in markets]
        except SQLAlchemyError as e:
            print(f"Database error getting markets for province {province_id}: {e}")
            return []

    @staticmethod
    def get_by_municipality(municipio_nome: str) -> List[Dict[str, Any]]:
        """
        Get all markets for a specific municipality.
        
        Args:
            municipio_nome: Name of the municipality
            
        Returns:
            List[Dict]: List of markets in the municipality
        """
        try:
            with get_db_session() as session:
                markets = session.query(Market).filter(
                    Market.municipio == municipio_nome
                ).order_by(Market.nome).all()
                return [market.to_dict() for market in markets]
        except SQLAlchemyError as e:
            print(f"Database error getting markets for municipality '{municipio_nome}': {e}")
            return []

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new market.
        
        Args:
            data: Market data (nome, provincia_id, municipio, tipo, endereco)
            
        Returns:
            Dict or None: Created market data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                market = Market(
                    nome=data['nome'],
                    provincia_id=data['provincia_id'],
                    municipio=data.get('municipio'),
                    tipo=data.get('tipo'),
                    endereco=data.get('endereco')
                )
                session.add(market)
                session.flush()
                result = market.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error creating market: {e}")
            return None

    @staticmethod
    def update(market_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing market.
        
        Args:
            market_id: ID of the market to update
            data: Updated market data
            
        Returns:
            Dict or None: Updated market data if successful, None otherwise
        """
        try:
            with get_db_session() as session:
                market = session.query(Market).filter(
                    Market.id == market_id
                ).first()
                
                if not market:
                    return None
                
                # Update fields if provided
                if 'nome' in data:
                    market.nome = data['nome']
                if 'provincia_id' in data:
                    market.provincia_id = data['provincia_id']
                if 'municipio' in data:
                    market.municipio = data['municipio']
                if 'tipo' in data:
                    market.tipo = data['tipo']
                if 'endereco' in data:
                    market.endereco = data['endereco']
                
                session.flush()
                result = market.to_dict()
                return result
        except SQLAlchemyError as e:
            print(f"Database error updating market {market_id}: {e}")
            return None

    @staticmethod
    def delete(market_id: int) -> bool:
        """
        Delete a market by ID.
        
        Args:
            market_id: ID of the market to delete
            
        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            with get_db_session() as session:
                market = session.query(Market).filter(
                    Market.id == market_id
                ).first()
                
                if not market:
                    return False
                
                session.delete(market)
                return True
        except SQLAlchemyError as e:
            print(f"Database error deleting market {market_id}: {e}")
            return False

    @staticmethod
    def count() -> int:
        """
        Get total count of markets.
        
        Returns:
            int: Total number of markets
        """
        try:
            with get_db_session() as session:
                return session.query(Market).count()
        except SQLAlchemyError as e:
            print(f"Database error counting markets: {e}")
            return 0
