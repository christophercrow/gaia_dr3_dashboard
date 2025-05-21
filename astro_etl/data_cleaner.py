"""
astro_etl/data_cleaner.py

Cleans and transforms raw Gaia DR3 data for scientific analysis and database loading.
Includes validation, quality filtering, and derived astrophysical fields.

Author: Your Name
Date: 2025-05-21
"""

import logging
import pandas as pd
from typing import TYPE_CHECKING

from astro_etl.utils.transformations import (
    parallax_to_distance,
    compute_abs_mag_g,
    total_proper_motion,
)

if TYPE_CHECKING:
    from astro_etl.config import Config

def clean_and_transform(df: pd.DataFrame, config: "Config") -> pd.DataFrame:
    """
    Clean, validate, and transform Gaia DR3 data.

    Steps:
    - Drop rows missing critical values (RA, Dec, G mag).
    - Handle non-physical/negative parallaxes.
    - Compute distance (pc), absolute magnitude, total proper motion.
    - Apply optional quality filters (e.g., parallax_over_error).
    - Remove duplicates by source_id.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw Gaia data from fetcher.
    config : Config
        Pipeline configuration (for filter/quality settings).

    Returns
    -------
    pd.DataFrame
        Cleaned and enriched DataFrame, ready for loading.
    """
    logging.info("Cleaning Gaia data...")
    # Drop rows with critical missing data
    df = df.dropna(subset=["ra", "dec", "phot_g_mean_mag"])
    # Set negative/zero parallax to NaN
    if "parallax" in df.columns:
        df["parallax"] = df["parallax"].where(df["parallax"] > 0)
    # Calculate distance in parsecs (NaN/inf for bad parallaxes)
    df["distance_pc"] = parallax_to_distance(df["parallax"].values)
    # Compute absolute G magnitude (using distance)
    df["abs_mag_g"] = compute_abs_mag_g(df["phot_g_mean_mag"].values, df["distance_pc"].values)
    # Calculate total proper motion
    df["pmra"] = df.get("pmra", 0).fillna(0)
    df["pmdec"] = df.get("pmdec", 0).fillna(0)
    df["pm_total"] = total_proper_motion(df["pmra"].values, df["pmdec"].values)
    # Optional: Apply quality filters if configured
    if config.quality.get("parallax_over_error_min") and "parallax_error" in df.columns:
        poe = config.quality["parallax_over_error_min"]
        mask = (df["parallax"] / df["parallax_error"]) > poe
        before = len(df)
        df = df[mask]
        logging.info(f"Quality filter (parallax_over_error > {poe}) removed {before - len(df)} stars.")
    # Drop duplicates by source_id, keep first
    df = df.drop_duplicates(subset=["source_id"])
    df = df.reset_index(drop=True)
    logging.info(f"Cleaned dataset has {len(df)} stars.")
    return df
