"""
tests/test_cleaner.py

Unit tests for astro_etl.data_cleaner (clean_and_transform).
"""

import pandas as pd
from astro_etl.data_cleaner import clean_and_transform

class DummyConfig:
    # Mimics minimal config interface for cleaner
    quality = {}

def test_clean_and_transform_basic():
    df = pd.DataFrame({
        "source_id": [1, 2, 3],
        "ra": [100.0, 200.0, 300.0],
        "dec": [0.0, -30.0, 45.0],
        "parallax": [10.0, 0.0, -5.0],  # 2nd, 3rd are bad
        "phot_g_mean_mag": [10.5, 11.2, 12.1],
        "bp_rp": [0.8, 1.5, 1.2],
        "pmra": [5.0, 0.0, None],
        "pmdec": [2.0, None, 0.0]
    })
    cleaned = clean_and_transform(df, DummyConfig())
    assert "distance_pc" in cleaned
    assert "abs_mag_g" in cleaned
    assert "pm_total" in cleaned
    # Only one good parallax
    assert cleaned["distance_pc"].iloc[0] == 100
    assert cleaned.shape[0] == 3  # We keep rows with nonphysical parallax but set their distance to inf

def test_removes_duplicates():
    df = pd.DataFrame({
        "source_id": [1, 1, 2],
        "ra": [10, 10, 20],
        "dec": [0, 0, 1],
        "parallax": [5, 5, 10],
        "phot_g_mean_mag": [10, 10, 11],
        "bp_rp": [1.0, 1.0, 1.1],
        "pmra": [1, 1, 1],
        "pmdec": [1, 1, 1]
    })
    cleaned = clean_and_transform(df, DummyConfig())
    assert cleaned["source_id"].is_unique
    assert cleaned.shape[0] == 2
