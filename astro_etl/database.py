"""
astro_etl/database.py

Database engine and session factory for the Gaia DR3 ETL project.
Uses SQLAlchemy for flexible backend support (PostgreSQL, SQLite for testing).

"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

def get_engine(db_url: str = None):
    """
    Create a SQLAlchemy engine.

    Parameters
    ----------
    db_url : str, optional
        Database URL (SQLAlchemy format). If None, loads from env DATABASE_URL.

    Returns
    -------
    sqlalchemy.engine.Engine
    """
    if db_url is None:
        db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("Database URL must be provided via argument or DATABASE_URL env var.")
    return create_engine(db_url, echo=False, future=True)

def get_session(engine) -> Session:
    """
    Create a new SQLAlchemy session.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        The SQLAlchemy engine to bind the session to.

    Returns
    -------
    sqlalchemy.orm.Session
    """
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    return SessionLocal()
