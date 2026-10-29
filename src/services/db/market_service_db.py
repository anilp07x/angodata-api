"""
Market service using SQLAlchemy ORM.
Provides database-backed operations for markets.
"""

from typing import Any, Dict, List, Optional

from sqlalchemy.orm import joinedload

from src.database.base import get_db_session
from src.database.models import Market
from src.services.db.common import resolve_location


class MarketServiceDB:
    """Service for managing markets with PostgreSQL database."""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all markets from database."""
        with get_db_session() as session:
            markets = (
                session.query(Market)
                .options(joinedload(Market.province), joinedload(Market.municipality))
                .order_by(Market.nome)
                .all()
            )
            return [market.to_dict() for market in markets]

    @staticmethod
    def get_by_id(market_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific market by ID."""
        with get_db_session() as session:
            market = (
                session.query(Market)
                .options(joinedload(Market.province), joinedload(Market.municipality))
                .filter(Market.id == market_id)
                .first()
            )
            return market.to_dict() if market else None

    @staticmethod
    def get_by_province(province_id: int) -> List[Dict[str, Any]]:
        """Get all markets for a specific province."""
        with get_db_session() as session:
            markets = (
                session.query(Market)
                .options(joinedload(Market.province), joinedload(Market.municipality))
                .filter(Market.provincia_id == province_id)
                .order_by(Market.nome)
                .all()
            )
            return [market.to_dict() for market in markets]

    @staticmethod
    def get_by_municipality(municipio_id: int) -> List[Dict[str, Any]]:
        """Get all markets for a specific municipality (by municipality ID)."""
        with get_db_session() as session:
            markets = (
                session.query(Market)
                .options(joinedload(Market.province), joinedload(Market.municipality))
                .filter(Market.municipio_id == int(municipio_id))
                .order_by(Market.nome)
                .all()
            )
            return [market.to_dict() for market in markets]

    @staticmethod
    def create(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new market (validates province/municipality relationship)."""
        with get_db_session() as session:
            location = resolve_location(
                session, data["provincia_id"], data.get("municipio_id")
            )
            if not location:
                return None

            provincia_nome, municipio_id, municipio_nome = location
            market = Market(
                nome=data["nome"],
                tipo=data.get("tipo"),
                provincia_id=data["provincia_id"],
                municipio_id=municipio_id,
                municipio=municipio_nome,
                especialidade=data.get("especialidade"),
                endereco=data.get("endereco"),
            )
            session.add(market)
            session.flush()
            result = market.to_dict()
            result["provincia_nome"] = provincia_nome
            return result

    @staticmethod
    def update(market_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an existing market (validates province/municipality relationship)."""
        with get_db_session() as session:
            market = (
                session.query(Market)
                .options(joinedload(Market.province), joinedload(Market.municipality))
                .filter(Market.id == market_id)
                .first()
            )

            if not market:
                return None

            # Atualizar província/município (validar antes de mutar o modelo)
            location = None
            if "provincia_id" in data or "municipio_id" in data:
                provincia_id = data.get("provincia_id", market.provincia_id)
                municipio_id = data.get("municipio_id", market.municipio_id)

                location = resolve_location(session, provincia_id, municipio_id)
                if not location:
                    return None

                provincia_nome, municipio_id, municipio_nome = location
                market.provincia_id = provincia_id
                market.municipio_id = municipio_id
                market.municipio = municipio_nome

            if "nome" in data:
                market.nome = data["nome"]
            if "tipo" in data:
                market.tipo = data["tipo"]
            if "especialidade" in data:
                market.especialidade = data["especialidade"]
            if "endereco" in data:
                market.endereco = data["endereco"]

            session.flush()
            result = market.to_dict()
            if location is not None:
                result["provincia_nome"] = provincia_nome
            return result

    @staticmethod
    def delete(market_id: int) -> bool:
        """Delete a market by ID."""
        with get_db_session() as session:
            market = session.query(Market).filter(Market.id == market_id).first()

            if not market:
                return False

            session.delete(market)
            return True

    @staticmethod
    def count() -> int:
        """Get total count of markets."""
        with get_db_session() as session:
            return session.query(Market).count()
