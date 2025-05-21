"""
astro_etl/config.py

Configuration loader for Gaia DR3 ETL pipeline.
Loads pipeline parameters from YAML and .env files for reproducible and flexible runs.
"""

import os
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO)


class Config:
    """
    Container for all pipeline configuration parameters.
    
    Attributes
    ----------
    db_url : str
        SQLAlchemy/Postgres connection URL.
    region : dict
        Dictionary with sky selection parameters (center_ra, center_dec, radius).
    phot_g_mean_mag_max : float
        Upper G-band magnitude limit for fetched stars.
    parallax_min : float
        Minimum parallax (mas) for fetched stars.
    limit : int
        Row limit for query.
    quality : dict
        Dict for quality/filter settings (e.g., parallax_over_error_min).
    dump_to_file : bool
        Whether to cache fetched raw data locally.
    """

    def __init__(
        self,
        config_path: str = "config.yaml",
        env_path: str = ".env"
    ):
        # Load .env for DB and secrets
        load_dotenv(env_path)
        # Parse YAML config
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        # Priority: env var > YAML config > default
        self.db_url: str = os.getenv("DATABASE_URL", config.get("db_url", ""))
        self.region: Dict[str, Any] = config.get("region", {})
        self.phot_g_mean_mag_max: float = float(config.get("phot_g_mean_mag_max", 15.0))
        self.parallax_min: float = float(config.get("parallax_min", 0.0))
        self.limit: int = int(config.get("limit", 10000))
        self.quality: Dict[str, Any] = config.get("quality", {})
        self.dump_to_file: bool = bool(config.get("dump_to_file", True))

def load_config(
    config_path: str = "config.yaml", env_path: str = ".env"
) -> Config:
    """
    Loads pipeline configuration from disk.

    Parameters
    ----------
    config_path : str
        Path to YAML config file.
    env_path : str
        Path to .env file.

    Returns
    -------
    Config
        An instance of the Config class with loaded parameters.
    """
    return Config(config_path, env_path)

if __name__ == "__main__":
    from astro_etl.config import Config
    import pandas as pd

    config = Config("config.yaml", ".env")
    # If your cleaner saves to 'data/cleaned_gaia.csv', load it:
    df = pd.read_csv("data/raw_gaia.csv")  # or cleaned_gaia.csv if you clean data!
    load_to_db(df, config.db_url)
