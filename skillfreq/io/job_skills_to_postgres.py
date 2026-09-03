from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor, execute_values

from skillfreq.skills.job_market import (
    extract_job_rows,
    load_market_taxonomy,
    make_job_key,
    taxonomy_version,
)


@dataclass(frozen=True)
class JobSkillRefreshResult:
    jobs_processed: int
    skill_rows_written: int
    taxonomy_version: str


ProgressCallback = Callable[[str], None]


def _connect(connect_timeout: int, statement_timeout: int, lock_timeout: int):
    load_dotenv()
    if database_url := os.getenv("DATABASE_URL"):
        connection = psycopg2.connect(
            database_url,
            connect_timeout=connect_timeout,
        )
    else:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", "5432"),
            connect_timeout=connect_timeout,
        )
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT set_config('statement_timeout', %s, false)",
            (f"{statement_timeout}s",),
        )
        cursor.execute(
            "SELECT set_config('lock_timeout', %s, false)",
            (f"{lock_timeout}s",),
        )
    return connection


def refresh_job_skills(
    taxonomy_path: Path,
    schema_path: Path,
    on_progress: ProgressCallback | None = None,
    connect_timeout: int = 10,
    statement_timeout: int = 120,
    lock_timeout: int = 10,
    since_days: int | None = None,
    limit: int | None = None,
) -> JobSkillRefreshResult:
    """Atomically rebuild job_skills from the current clean_jobs result set."""
    report = on_progress or (lambda _message: None)
    report("Loading the market-skill taxonomy")
    taxonomy = load_market_taxonomy(taxonomy_path)
    version = taxonomy_version(taxonomy_path)

    report("Connecting to PostgreSQL")
    with _connect(connect_timeout, statement_timeout, lock_timeout) as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            report("Preparing job-skill tables and views")
            cursor.execute(schema_path.read_text(encoding="utf-8"))
            report("Reading clean jobs")
            query = """
                SELECT source_site, source_job_id, job_url, description
                FROM public.clean_jobs
            """
            parameters: list[object] = []
            if since_days is not None:
                query += " WHERE date_posted >= CURRENT_DATE - %s"
                parameters.append(since_days)
            query += " ORDER BY date_posted DESC NULLS LAST, source_site, source_job_id, job_url"
            if limit is not None:
                query += " LIMIT %s"
                parameters.append(limit)
            cursor.execute(query, parameters)
            jobs = cursor.fetchall()
            report(f"Extracting normalized skills from {len(jobs):,} jobs")
            rows = extract_job_rows(jobs, taxonomy)

            report(f"Writing {len(rows):,} normalized job-skill rows")
            cursor.execute(
                """
                INSERT INTO public.job_skill_extraction_runs (taxonomy_version)
                VALUES (%s)
                RETURNING run_id
                """,
                (version,),
            )
            run_id = cursor.fetchone()["run_id"]
            cursor.execute("DELETE FROM public.market_skill_taxonomy")
            execute_values(
                cursor,
                """
                INSERT INTO public.market_skill_taxonomy (
                    canonical_skill, aliases, taxonomy_version
                ) VALUES %s
                """,
                [(skill, aliases, version) for skill, aliases in taxonomy.items()],
            )
            cursor.execute("DELETE FROM public.job_skills")
            cursor.execute("DELETE FROM public.job_skill_scope")
            if jobs:
                execute_values(
                    cursor,
                    """
                    INSERT INTO public.job_skill_scope (
                        job_key, source_site, source_job_id, job_url,
                        extraction_run_id
                    ) VALUES %s
                    """,
                    [
                        (
                            make_job_key(
                                job.get("source_site"),
                                job.get("source_job_id"),
                                job.get("job_url"),
                            ),
                            job.get("source_site"),
                            job.get("source_job_id"),
                            job.get("job_url"),
                            run_id,
                        )
                        for job in jobs
                    ],
                    page_size=1000,
                )
            if rows:
                execute_values(
                    cursor,
                    """
                    INSERT INTO public.job_skills (
                        job_key, source_site, source_job_id, job_url,
                        canonical_skill, matched_terms, mention_count,
                        extraction_run_id
                    ) VALUES %s
                    """,
                    [row + (run_id,) for row in rows],
                    page_size=1000,
                )
            cursor.execute(
                """
                UPDATE public.job_skill_extraction_runs
                SET completed_at = now(), jobs_processed = %s, skill_rows_written = %s
                WHERE run_id = %s
                """,
                (len(jobs), len(rows), run_id),
            )

    report("Refresh complete")
    return JobSkillRefreshResult(len(jobs), len(rows), version)
