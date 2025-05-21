"""
tests/test_fetcher.py

Unit test for astro_etl.data_fetcher.build_adql_query.
"""

from astro_etl.config import Config
from astro_etl.data_fetcher import build_adql_query

def test_build_adql_query_output():
    cfg = Config()
    cfg.region = {"center_ra": 10.0, "center_dec": 5.0, "radius": 1.0}
    cfg.phot_g_mean_mag_max = 12.0
    cfg.parallax_min = 1.0
    cfg.limit = 100
    query = build_adql_query(cfg)
    assert "CIRCLE('ICRS', 10.0, 5.0, 1.0)" in query
    assert "phot_g_mean_mag < 12.0" in query
    assert "parallax > 1.0" in query
    assert "LIMIT 100" in query
