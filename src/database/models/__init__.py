"""
SQLAlchemy models for AngoData API.
"""

import enum
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database.base import Base


class UserRole(enum.Enum):
    """User roles for authorization."""

    admin = "admin"
    editor = "editor"
    user = "user"


class User(Base):
    """User model for authentication and authorization."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.user)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Convert model to dictionary (excluding password)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value if isinstance(self.role, UserRole) else self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"


class Province(Base):
    """Province (Província) model."""

    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True, index=True)
    capital = Column(String(100))
    area_km2 = Column(Float)
    populacao = Column(Integer)

    # Relationships
    municipalities = relationship("Municipality", back_populates="province", cascade="all, delete-orphan")
    schools = relationship("School", back_populates="province", cascade="all, delete-orphan")
    markets = relationship("Market", back_populates="province", cascade="all, delete-orphan")
    hospitals = relationship("Hospital", back_populates="province", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "nome": self.nome,
            "capital": self.capital,
            "area_km2": self.area_km2,
            "populacao": self.populacao,
        }

    def __repr__(self):
        return f"<Province(id={self.id}, nome='{self.nome}')>"


class Municipality(Base):
    """Municipality (Município) model."""

    __tablename__ = "municipalities"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)
    provincia_id = Column(Integer, ForeignKey("provinces.id"), nullable=False, index=True)
    area_km2 = Column(Float)
    populacao = Column(Integer)

    # Relationships
    province = relationship("Province", back_populates="municipalities")

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "nome": self.nome,
            "provincia_id": self.provincia_id,
            "area_km2": self.area_km2,
            "populacao": self.populacao,
        }

    def __repr__(self):
        return f"<Municipality(id={self.id}, nome='{self.nome}')>"


class School(Base):
    """School (Escola) model."""

    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False, index=True)
    provincia_id = Column(Integer, ForeignKey("provinces.id"), nullable=False, index=True)
    municipio = Column(String(100))
    tipo = Column(String(50))  # primário, secundário, técnico, etc.
    nivel = Column(String(50))  # ensino primário, médio, técnico, etc.

    # Relationships
    province = relationship("Province", back_populates="schools")

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "nome": self.nome,
            "provincia_id": self.provincia_id,
            "municipio": self.municipio,
            "tipo": self.tipo,
            "nivel": self.nivel,
        }

    def __repr__(self):
        return f"<School(id={self.id}, nome='{self.nome}')>"


class Market(Base):
    """Market (Mercado) model."""

    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False, index=True)
    provincia_id = Column(Integer, ForeignKey("provinces.id"), nullable=False, index=True)
    municipio = Column(String(100))
    tipo = Column(String(50))  # municipal, informal, grossista, etc.
    endereco = Column(String(255))

    # Relationships
    province = relationship("Province", back_populates="markets")

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "nome": self.nome,
            "provincia_id": self.provincia_id,
            "municipio": self.municipio,
            "tipo": self.tipo,
            "endereco": self.endereco,
        }

    def __repr__(self):
        return f"<Market(id={self.id}, nome='{self.nome}')>"


class Hospital(Base):
    """Hospital model."""

    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False, index=True)
    provincia_id = Column(Integer, ForeignKey("provinces.id"), nullable=False, index=True)
    municipio = Column(String(100))
    tipo = Column(String(50))  # central, provincial, municipal, posto de saúde, etc.
    endereco = Column(String(255))
    especialidades = Column(String(500))  # Comma-separated list

    # Relationships
    province = relationship("Province", back_populates="hospitals")

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "nome": self.nome,
            "provincia_id": self.provincia_id,
            "municipio": self.municipio,
            "tipo": self.tipo,
            "endereco": self.endereco,
            "especialidades": self.especialidades,
        }

    def __repr__(self):
        return f"<Hospital(id={self.id}, nome='{self.nome}')>"
