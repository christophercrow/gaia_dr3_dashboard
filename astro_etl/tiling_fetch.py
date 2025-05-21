"""
astro_etl/tiling_fetch.py

Fetches Gaia DR3 data over a large sky area by tiling small cone searches.
Merges and deduplicates results. Science-scale friendly.

Author: Your Name
Date: 2025-05-21
"""

import os
import time
import logging
import pandas as pd
from astroquery.gaia import Gaia

def make_tile_centers(center_ra, center_dec, width, height, tile_radius):
    """
    Generate a grid of tile centers for given sky box and tile size.

    Returns a list of (ra, dec) tuples.
    """
    ras = []
    decs = []
    n_ra = int(width // (tile_radius * 1.8))  # Small overlap
    n_dec = int(height // (tile_radius * 1.8))
    ra_start = center_ra - width / 2
    dec_start = center_dec - height / 2
    for i in range(n_ra + 1):
        ra = ra_start + i * tile_radius * 1.7  # Overlap ~0.7*radius
        for j in range(n_dec + 1):
            dec = dec_start + j * tile_radius * 1.7
            if dec >= -90 and dec <= 90:
                ras.append(ra)
                decs.append(dec)
    return list(zip(ras, decs))

def fetch_tile(ra, dec, radius, mag_limit=17.0, parallax_min=0.0, row_limit=5000):
    query = f"""
    SELECT source_id, ra, dec, parallax, phot_g_mean_mag, bp_rp, pmra, pmdec
    FROM gaiadr3.gaia_source
    WHERE CONTAINS(
        POINT('ICRS', ra, dec),
        CIRCLE('ICRS', {ra}, {dec}, {radius})
    ) = 1
      AND phot_g_mean_mag < {mag_limit}
      AND parallax > {parallax_min}
    LIMIT {row_limit}
    """
    logging.info(f"Fetching tile at RA={ra:.3f}, Dec={dec:.3f}")
    job = Gaia.launch_job_async(query)
    tbl = job.get_results()
    return tbl.to_pandas()

    tile_fetch_pipeline(
        center_ra=100.0,
        center_dec=20.0,
        width=2.0,        # Keep this small for now
        height=2.0,
        tile_radius=0.2,  # Smaller tiles
        mag_limit=16.0,
        parallax_min=0.0,
        row_limit=2000,   # Fewer stars per tile
        sleep=4,          # Wait longer between queries
        out_csv="data/tiling_gaia.csv"
    )

    os.makedirs("data", exist_ok=True)
    tile_centers = make_tile_centers(center_ra, center_dec, width, height, tile_radius)
    all_dfs = []
    for idx, (ra, dec) in enumerate(tile_centers):
        try:
            df = fetch_tile(
                ra, dec, tile_radius, mag_limit, parallax_min, row_limit
            )
            all_dfs.append(df)
        except Exception as e:
            logging.error(f"Tile at RA={ra}, Dec={dec} failed: {e}")
        time.sleep(sleep)  # Be gentle to TAP server!
    if all_dfs:
        all_stars = pd.concat(all_dfs, ignore_index=True)
        all_stars = all_stars.drop_duplicates(subset="source_id")
        all_stars.to_csv(out_csv, index=False)
        print(f"Tiled fetch complete. Saved {len(all_stars)} stars to {out_csv}")
    else:
        print("No data fetched!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # EXAMPLE: Fetch a 4°x4° patch centered at RA=100°, Dec=20° in tiles of 0.5°
    tile_fetch_pipeline(
        center_ra=100.0,
        center_dec=20.0,
        width=4.0,
        height=4.0,
        tile_radius=0.5,
        mag_limit=17.0,
        parallax_min=0.0,
        row_limit=5000,  # Each cone fetch
        sleep=2,         # Wait between queries
        out_csv="data/tiling_gaia.csv"
    )
