"""
SQLAlchemy models for AngoData API.
"""

import enum
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float, ForeignKey, Integer, String, UniqueConstraint
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
    username = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        SQLEnum(UserRole, name="userrole", values_callable=lambda e: [m.value for m in e]),
        nullable=False,
        default=UserRole.user,
    )
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
    municipalities = relationship(
        "Municipality", back_populates="province", cascade="all, delete-orphan"
    )
    schools = relationship(
        "School", back_populates="province", cascade="all, delete-orphan"
    )
    markets = relationship(
        "Market", back_populates="province", cascade="all, delete-orphan"
    )
    hospitals = relationship(
        "Hospital", back_populates="province", cascade="all, delete-orphan"
    )

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
    __table_args__ = (UniqueConstraint("nome", "provincia_id", name="uq_municipality_nome_provincia"),)

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)
    provincia_id = Column(Integer, ForeignKey("provinces.id"), nullable=False, index=True)
    area_km2 = Column(Float)
    populacao = Column(Integer)

    # Relationships
    province = relationship("Province", back_populates="municipalities")
    schools = relationship(
        "School", back_populates="municipality", cascade="all, delete-orphan"
    )
    markets = relationship(
        "Market", back_populates="municipality", cascade="all, delete-orphan"
    )
    hospitals = relationship(
        "Hospital", back_populates="municipality", cascade="all, delete-orphan"
    )

    @property
    def provincia_nome(self):
        """Name of the parent province (requires loaded relationship)."""
        return self.province.nome if self.province is not None else None

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "nome": self.nome,
            "provincia_id": self.provincia_id,
            "provincia_nome": self.provincia_nome,
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
    tipo = Column(String(50))  # pública, privada, etc.
    provincia_id = Column(Integer, ForeignKey("provinces.id"), nullable=False, index=True)
    municipio_id = Column(Integer, ForeignKey("municipalities.id"), index=True)
    municipio = Column(String(100))  # Nome string para compatibilidade
    nivel = Column(String(50))  # ensino primário, médio, técnico, etc.
    endereco = Column(String(255))

    # Relationships
    province = relationship("Province", back_populates="schools")
    municipality = relationship("Municipality", back_populates="schools")

    @property
    def provincia_nome(self):
        """Name of the parent province (requires loaded relationship)."""
        return self.province.nome if self.province is not None else None

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo,
            "provincia_id": self.provincia_id,
            "provincia_nome": self.provincia_nome,
            "municipio_id": self.municipio_id,
            "municipio": self.municipio,
            "nivel": self.nivel,
            "endereco": self.endereco,
        }

    def __repr__(self):
        return f"<School(id={self.id}, nome='{self.nome}')>"


class Market(Base):
    """Market (Mercado) model."""

    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False, index=True)
    tipo = Column(String(50))  # municipal, informal, grossista, etc.
    provincia_id = Column(Integer, ForeignKey("provinces.id"), nullable=False, index=True)
    municipio_id = Column(Integer, ForeignKey("municipalities.id"), index=True)
    municipio = Column(String(100))  # Nome string para compatibilidade
    especialidade = Column(String(255))
    endereco = Column(String(255))

    # Relationships
    province = relationship("Province", back_populates="markets")
    municipality = relationship("Municipality", back_populates="markets")

    @property
    def provincia_nome(self):
        """Name of the parent province (requires loaded relationship)."""
        return self.province.nome if self.province is not None else None

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo,
            "provincia_id": self.provincia_id,
            "provincia_nome": self.provincia_nome,
            "municipio_id": self.municipio_id,
            "municipio": self.municipio,
            "especialidade": self.especialidade,
            "endereco": self.endereco,
        }

    def __repr__(self):
        return f"<Market(id={self.id}, nome='{self.nome}')>"


class Hospital(Base):
    """Hospital model."""

    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False, index=True)
    tipo = Column(String(50))  # central, provincial, municipal, posto de saúde, etc.
    categoria = Column(String(50))  # geral, especializado, etc.
    provincia_id = Column(Integer, ForeignKey("provinces.id"), nullable=False, index=True)
    municipio_id = Column(Integer, ForeignKey("municipalities.id"), index=True)
    municipio = Column(String(100))  # Nome string para compatibilidade
    endereco = Column(String(255))
    especialidades = Column(String(500))  # Comma-separated list

    # Relationships
    province = relationship("Province", back_populates="hospitals")
    municipality = relationship("Municipality", back_populates="hospitals")

    @property
    def provincia_nome(self):
        """Name of the parent province (requires loaded relationship)."""
        return self.province.nome if self.province is not None else None

    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "nome": self.nome,
            "tipo": self.tipo,
            "categoria": self.categoria,
            "provincia_id": self.provincia_id,
            "provincia_nome": self.provincia_nome,
            "municipio_id": self.municipio_id,
            "municipio": self.municipio,
            "endereco": self.endereco,
            "especialidades": self.especialidades,
        }

    def __repr__(self):
        return f"<Hospital(id={self.id}, nome='{self.nome}')>"
