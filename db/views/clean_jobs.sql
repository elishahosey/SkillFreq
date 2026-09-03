DROP VIEW IF EXISTS public.clean_jobs;

CREATE VIEW public.clean_jobs AS
WITH normalized_jobs AS (
    SELECT
        NULLIF(BTRIM(id), '') AS source_job_id,
        NULLIF(BTRIM(site), '') AS source_site,
        source_file,
        CASE
            WHEN source_file ~ 'jobs-[0-9]{1,2}-[0-9]{1,2}-[0-9]{2}[.]csv$'
            THEN TO_DATE(
                SUBSTRING(
                    source_file
                    FROM 'jobs-([0-9]{1,2}-[0-9]{1,2}-[0-9]{2})[.]csv$'
                ),
                'MM-DD-YY'
            )
        END AS snapshot_date,
        date_posted::date AS date_posted,
        COALESCE(
            NULLIF(BTRIM(job_url_direct), ''),
            NULLIF(BTRIM(job_url), '')
        ) AS job_url,
        NULLIF(BTRIM(title), '') AS title,
        NULLIF(BTRIM(company), '') AS company,
        NULLIF(BTRIM(location), '') AS location,
        NULLIF(BTRIM(job_type), '') AS job_type,
        is_remote,
        NULLIF(BTRIM(description), '') AS description
    FROM staging.jobs
),
ranked_jobs AS (
    SELECT
        normalized_jobs.*,
        ROW_NUMBER() OVER (
            PARTITION BY
                source_site,
                COALESCE(source_job_id, job_url)
            ORDER BY
                snapshot_date DESC NULLS LAST,
                date_posted DESC NULLS LAST,
                source_file DESC NULLS LAST
        ) AS dedupe_rank
    FROM normalized_jobs
    WHERE title IS NOT NULL
      AND company IS NOT NULL
      AND description IS NOT NULL
)
SELECT
    source_job_id,
    source_site,
    source_file,
    snapshot_date,
    date_posted,
    job_url,
    title,
    company,
    location,
    job_type,
    is_remote,
    description
FROM ranked_jobs
WHERE dedupe_rank = 1;

COMMENT ON VIEW public.clean_jobs IS
    'One row per unique staging.jobs source posting, normalized and deduplicated for skill analysis.';
