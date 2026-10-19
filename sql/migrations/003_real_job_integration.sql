-- ============================================================
-- Career Intelligence Platform
-- MVP 1C - Real Job Integration
-- ============================================================

BEGIN;

CREATE UNIQUE INDEX uq_job_posting_source
ON fact_job_posting (source_name, source_job_id)
WHERE source_name IS NOT NULL
  AND source_job_id IS NOT NULL;

COMMIT;