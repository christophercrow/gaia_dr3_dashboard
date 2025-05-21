"""
astro_etl/data_fetcher.py

Fetches Gaia DR3 data using ADQL via astroquery.
Supports region, magnitude, parallax, and row limit filters, with robust error handling.

Author: Your Name
Date: 2025-05-21
"""

import logging
import pandas as pd
from astroquery.gaia import Gaia
from astro_etl.config import Config
from astro_etl.utils.logging_util import setup_logging

import logging
from astroquery.gaia import Gaia
from astro_etl.config import Config
import pandas as pd

def build_adql_query(config: Config) -> str:
    """
    Constructs an ADQL query string from configuration.

    Parameters
    ----------
    config : Config
        Configuration object.

    Returns
    -------
    query : str
        ADQL query string.
    """
    region = config.region
    ra, dec, radius = region.get("center_ra"), region.get("center_dec"), region.get("radius")
    query = f"""
    SELECT source_id, ra, dec, parallax, phot_g_mean_mag, bp_rp, pmra, pmdec
    FROM gaiadr3.gaia_source
    WHERE CONTAINS(
        POINT('ICRS', ra, dec),
        CIRCLE('ICRS', {ra}, {dec}, {radius})
    ) = 1
      AND phot_g_mean_mag < {config.phot_g_mean_mag_max}
      AND parallax > {config.parallax_min}
    ORDER BY source_id
    """
    logging.info(f"Query being sent:\n{query}")
    return query

def fetch_gaia_data(config: Config, output_csv: str = "data/raw_gaia.csv") -> pd.DataFrame:    
    """
    Fetches Gaia data using astroquery.gaia.

    Parameters
    ----------
    config : Config
        Configuration object.

    Returns
    -------
    df : pd.DataFrame
        DataFrame containing the fetched Gaia data.
    """
    query = build_adql_query(config)
    try:
        job = Gaia.launch_job_async(query)
        result = job.get_results()
        df = result.to_pandas()
        if output_csv is not None:
            import os
            os.makedirs(os.path.dirname(output_csv), exist_ok=True)
            df.to_csv(output_csv, index=False)
        return df
    except Exception as e:
        logging.error(f"Failed to fetch Gaia data: {e}")
        raise RuntimeError("Error in Gaia data fetch") from e

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = Config("config.yaml", ".env")
    try:
        fetch_gaia_data(config, output_csv="data/raw_gaia.csv")
    except Exception as e:
        logging.error(f"ETL fetcher failed: {e}")
