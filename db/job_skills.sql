CREATE TABLE IF NOT EXISTS public.job_skill_extraction_runs (
    run_id bigserial PRIMARY KEY,
    started_at timestamptz NOT NULL DEFAULT now(),
    completed_at timestamptz,
    taxonomy_version text NOT NULL,
    jobs_processed integer,
    skill_rows_written integer
);

CREATE TABLE IF NOT EXISTS public.market_skill_taxonomy (
    canonical_skill text PRIMARY KEY,
    aliases text[] NOT NULL,
    taxonomy_version text NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.job_skills (
    job_key text NOT NULL,
    source_site text,
    source_job_id text,
    job_url text,
    canonical_skill text NOT NULL,
    matched_terms text[] NOT NULL,
    mention_count integer NOT NULL CHECK (mention_count > 0),
    extraction_run_id bigint NOT NULL
        REFERENCES public.job_skill_extraction_runs(run_id),
    extracted_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (job_key, canonical_skill)
);

CREATE TABLE IF NOT EXISTS public.job_skill_scope (
    job_key text PRIMARY KEY,
    source_site text,
    source_job_id text,
    job_url text,
    extraction_run_id bigint NOT NULL
        REFERENCES public.job_skill_extraction_runs(run_id)
);

CREATE INDEX IF NOT EXISTS job_skills_canonical_skill_idx
    ON public.job_skills (canonical_skill);

COMMENT ON TABLE public.job_skills IS
    'One row per deduplicated job and canonical skill. matched_terms preserves extraction evidence.';

-- Dashboard-ready semantic layer. Every in-scope clean job is paired with every
-- configured skill, including skills the job does not mention. Filtering these
-- rows first and grouping second guarantees that numerator and denominator use
-- one population.
--
-- The primary analysis intentionally uses the broad job spectrum selected by the
-- refresh. Role/title filters are optional comparison slices, not an assumption
-- built into this view. Skill percentages overlap: a job may contribute once to
-- SQL prevalence and once to Python prevalence, so percentages are not additive.
CREATE OR REPLACE VIEW public.job_skill_prevalence_input AS
SELECT
    cj.source_job_id,
    cj.source_site,
    cj.source_file,
    cj.snapshot_date,
    cj.date_posted,
    cj.job_url,
    cj.title,
    cj.company,
    cj.location,
    cj.job_type,
    cj.is_remote,
    taxonomy.canonical_skill,
    (js.job_key IS NOT NULL) AS mentions_skill
FROM public.clean_jobs cj
JOIN public.job_skill_scope scope
  ON scope.source_site IS NOT DISTINCT FROM cj.source_site
 AND COALESCE(scope.source_job_id, scope.job_url) = COALESCE(cj.source_job_id, cj.job_url)
CROSS JOIN public.market_skill_taxonomy taxonomy
LEFT JOIN public.job_skills js
  ON js.source_site IS NOT DISTINCT FROM cj.source_site
 AND COALESCE(js.source_job_id, js.job_url) = COALESCE(cj.source_job_id, cj.job_url)
 AND js.canonical_skill = taxonomy.canonical_skill;

COMMENT ON VIEW public.job_skill_prevalence_input IS
    'Dashboard semantic layer: one row per clean job and configured skill, with a mention flag. Apply relevance filters before aggregating.';

-- Broad baseline prevalence across every job in the current extraction scope.
CREATE OR REPLACE VIEW public.skill_prevalence AS
WITH prevalence AS (
    SELECT
        canonical_skill,
        COUNT(*) FILTER (WHERE mentions_skill)::bigint AS jobs_mentioning_skill,
        COUNT(*)::bigint AS relevant_jobs
    FROM public.job_skill_prevalence_input
    GROUP BY canonical_skill
)
SELECT
    canonical_skill,
    jobs_mentioning_skill,
    relevant_jobs AS total_jobs,
    ROUND(
        100.0 * jobs_mentioning_skill / NULLIF(relevant_jobs, 0),
        1
    ) AS prevalence_pct
FROM prevalence
ORDER BY prevalence_pct DESC, canonical_skill;

COMMENT ON VIEW public.skill_prevalence IS
    'Broad skill prevalence: in-scope jobs mentioning a skill divided by all jobs in the same extraction scope. Skill percentages overlap and are not additive.';
