"""
astro_etl/load_data.py

Loads cleaned Gaia DR3 data into a PostgreSQL database using SQLAlchemy ORM.
Handles batch inserts, schema creation, transaction safety, and logging.

Author: Your Name
Date: 2025-05-21
"""

import logging
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import insert
from astro_etl.models import GaiaSource, Base
from astro_etl.database import get_engine, get_session

logging.basicConfig(level=logging.INFO)

def load_to_db(df: pd.DataFrame, db_url: str) -> None:
    """
    Loads a DataFrame of Gaia DR3 sources into the database.
    Skips duplicate primary keys (source_id) using upsert logic.
    """
    logging.info("Starting load to database...")
    engine = get_engine(db_url)
    Base.metadata.create_all(engine)
    session = get_session(engine)
    try:
        valid_columns = {c.name for c in GaiaSource.__table__.columns}
        records = [
            {k: v for k, v in row.items() if k in valid_columns}
            for row in df.to_dict(orient="records")
        ]
        if not records:
            logging.warning("No records to insert.")
            return

        stmt = insert(GaiaSource).values(records)
        stmt = stmt.on_conflict_do_nothing(index_elements=['source_id'])
        session.execute(stmt)
        session.commit()
        logging.info(f"Upserted {len(records)} rows into gaia_source table (duplicates skipped).")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Database insert failed: {e}")
        raise RuntimeError(f"Failed to load data into DB: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    from astro_etl.config import Config

    config = Config("config.yaml", ".env")
    df = pd.read_csv("data/raw_gaia.csv")
    load_to_db(df, config.db_url)
