"""
tests/test_database.py

Test loading GaiaSource objects into an in-memory SQLite DB.
"""

import pandas as pd
from astro_etl.models import GaiaSource, Base
from astro_etl.database import get_engine, get_session

def test_load_and_query():
    # In-memory SQLite for safe/fast test
    engine = get_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = get_session(engine)
    df = pd.DataFrame({
        "source_id": [101, 102],
        "ra": [20.0, 21.0],
        "dec": [0.0, -5.0],
        "parallax": [10.0, 8.0],
        "phot_g_mean_mag": [11.1, 13.3],
        "bp_rp": [1.1, 2.1],
        "distance_pc": [100.0, 125.0],
        "abs_mag_g": [6.1, 7.3],
        "pmra": [5.0, 0.0],
        "pmdec": [1.0, 2.0],
        "pm_total": [5.1, 2.0]
    })
    objs = [GaiaSource(**row) for row in df.to_dict(orient="records")]
    session.bulk_save_objects(objs)
    session.commit()
    results = session.query(GaiaSource).all()
    assert len(results) == 2
    assert results[0].ra == 20.0
    session.close()
