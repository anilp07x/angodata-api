"""
Database configuration and base models for SQLAlchemy.
"""

import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# Create declarative base
Base = declarative_base()

# Global variables
engine = None
SessionLocal = None


def init_database():
    """
    Initialize database connection and create session factory.
    Must be called before using the database.
    """
    global engine, SessionLocal

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")

    # Create engine with connection pooling
    engine = create_engine(
        database_url,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=10,  # Number of connections to maintain
        max_overflow=20,  # Max additional connections
        echo=False,  # Set to True for SQL logging during debug
    )

    # Create session factory
    SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

    return engine


def get_db():
    """
    Get database session.
    Use with context manager or try/finally to ensure proper cleanup.

    Usage:
        with get_db() as db:
            result = db.query(Model).all()
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    """
    Context manager for database sessions.
    Automatically commits on success and rolls back on error.

    Usage:
        with get_db_session() as session:
            session.add(new_object)
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_all_tables():
    """
    Create all tables defined in models.
    Should only be used in development. Use Alembic migrations in production.
    """
    if engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    Base.metadata.create_all(bind=engine)


def drop_all_tables():
    """
    Drop all tables. USE WITH CAUTION!
    Only for development/testing.
    """
    if engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    Base.metadata.drop_all(bind=engine)


def close_database():
    """
    Close all database connections.
    Should be called when shutting down the application.
    """
    global SessionLocal, engine

    if SessionLocal:
        SessionLocal.remove()

    if engine:
        engine.dispose()
