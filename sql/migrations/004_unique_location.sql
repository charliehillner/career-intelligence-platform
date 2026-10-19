-- ============================================================
-- Career Intelligence Platform
-- MVP 1C - Unique Location Constraint
-- ============================================================

BEGIN;

CREATE UNIQUE INDEX uq_location_geography
ON dim_location (country, region, city)
NULLS NOT DISTINCT;

COMMIT;
