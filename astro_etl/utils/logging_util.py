"""
astro_etl/utils/logging_util.py

Utility for initializing consistent logging across the Gaia DR3 ETL project.
"""

import logging
from typing import Optional

def setup_logging(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    """
    Configure logging for the pipeline.

    Parameters
    ----------
    level : int
        Logging level (e.g., logging.INFO, logging.DEBUG).
    log_file : Optional[str]
        If provided, logs will also be written to this file.

    Notes
    -----
    - Uses a standard timestamped format.
    - Suppresses verbose SQLAlchemy engine logs by default.
    """
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s [%(module)s]: %(message)s",
        handlers=handlers,
        force=True,  # Ensures re-config on repeated calls (Python 3.8+)
    )
    # Quiet down SQLAlchemy's engine noise unless debugging
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
