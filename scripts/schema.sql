-- scripts/schema.sql

-- Schema for storing Gaia DR3 sources (used by loader and dashboard)
CREATE TABLE IF NOT EXISTS gaia_source (
    source_id BIGINT PRIMARY KEY,
    ra DOUBLE PRECISION NOT NULL,        -- Right Ascension [deg, ICRS]
    dec DOUBLE PRECISION NOT NULL,       -- Declination [deg, ICRS]
    parallax DOUBLE PRECISION,           -- Parallax [mas]
    phot_g_mean_mag DOUBLE PRECISION,    -- G mean magnitude
    bp_rp DOUBLE PRECISION,              -- BP - RP color [mag]
    distance_pc DOUBLE PRECISION,        -- Distance [pc, derived]
    abs_mag_g DOUBLE PRECISION,          -- Absolute G mag [derived]
    pmra DOUBLE PRECISION,               -- Proper motion in RA [mas/yr]
    pmdec DOUBLE PRECISION,              -- Proper motion in Dec [mas/yr]
    pm_total DOUBLE PRECISION,           -- Total proper motion [mas/yr]
    healpix INT                          -- HEALPix partition index (optional)
);
