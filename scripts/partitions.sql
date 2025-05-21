-- scripts/partitions.sql

-- Example: range partitioning by HEALPix index (optional)
-- Replace values with the HEALPix grid used for your region/data volume.

ALTER TABLE gaia_source
    PARTITION BY RANGE (healpix);

CREATE TABLE IF NOT EXISTS gaia_source_hp0 PARTITION OF gaia_source
    FOR VALUES FROM (0) TO (1000);

CREATE TABLE IF NOT EXISTS gaia_source_hp1 PARTITION OF gaia_source
    FOR VALUES FROM (1000) TO (2000);

-- Repeat as needed for your HEALPix resolution/data size.
