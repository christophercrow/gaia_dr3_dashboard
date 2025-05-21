-- scripts/migration_example.sql

-- Example: Add a new column for storing a user-computed field (future science cases)
ALTER TABLE gaia_source ADD COLUMN IF NOT EXISTS cluster_label TEXT;
COMMENT ON COLUMN gaia_source.cluster_label IS 'Open cluster/association label (if known)';
