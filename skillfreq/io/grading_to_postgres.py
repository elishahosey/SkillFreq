"""Reuse the existing market semantic view, DB connection and score history."""
from datetime import datetime, timezone
from pathlib import Path
from psycopg2.extras import Json, RealDictCursor

from .job_skills_to_postgres import _connect
from skillfreq.skills.job_market import make_job_key

SCHEMA_PATH = Path(__file__).resolve().parents[2] / 'db/grading.sql'


def load_jobs_for_grading(since_days=90, limit=None, *, connect_timeout=10,
                          statement_timeout=120, lock_timeout=10):
    """Read deduplicated postings by posting date using the existing clean_jobs view."""
    if since_days <= 0 or (limit is not None and limit <= 0):
        raise ValueError('since_days and limit must be greater than zero')
    query = '''SELECT source_job_id, source_site, job_url, title, description
        FROM public.clean_jobs
        WHERE date_posted >= CURRENT_DATE - %s
        ORDER BY date_posted DESC NULLS LAST, source_site, source_job_id, job_url'''
    parameters = [since_days]
    if limit is not None:
        query += ' LIMIT %s'
        parameters.append(limit)
    connection = _connect(connect_timeout, statement_timeout, lock_timeout)
    try:
        connection.commit()  # Finish the connection's timeout configuration transaction.
        connection.set_session(readonly=True)
        with connection, connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, parameters)
            return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def load_prevalence(expected_taxonomy_version=None):
    # One consistent snapshot prevents combining an old denominator and new run.
    connection = _connect(5, 30, 5)
    try:
        connection.commit()
        connection.set_session(isolation_level='REPEATABLE READ', readonly=True)
        with connection, connection.cursor() as cursor:
            cursor.execute("SELECT to_regclass('public.job_skill_scope')")
            if cursor.fetchone()[0] is None:
                raise ValueError('Market extraction scope is missing; run the existing refresh-job-skills migration')
            cursor.execute('SELECT DISTINCT taxonomy_version FROM public.market_skill_taxonomy')
            versions = [row[0] for row in cursor.fetchall()]
            if expected_taxonomy_version and versions != [expected_taxonomy_version]:
                raise ValueError('Market prevalence taxonomy differs from grading taxonomy; refresh-job-skills first')
            cursor.execute('SELECT canonical_skill, prevalence_pct, total_jobs FROM public.skill_prevalence')
            rows = cursor.fetchall()
            if not rows or not any(row[2] for row in rows):
                raise ValueError('Market extraction scope is empty; refresh-job-skills before learning analysis')
            cursor.execute('SELECT DISTINCT extraction_run_id FROM public.job_skill_scope ORDER BY extraction_run_id')
            runs = [row[0] for row in cursor.fetchall()]
        return {name: float(pct) for name, pct, _ in rows if pct is not None}, dict(
            source='public.skill_prevalence', taxonomy_versions=versions, extraction_run_ids=runs,
            total_jobs=max((row[2] for row in rows), default=0), read_at=datetime.now(timezone.utc).isoformat(),
            population='extraction_snapshot')
    finally:
        connection.close()


def register_configuration(cursor, context):
    from skillfreq.configuration import configuration_version
    if configuration_version(context.snapshot) != context.grading_version:
        raise ValueError('Configuration snapshot does not match its grading version')
    cursor.execute('''INSERT INTO public.grading_config_versions
        (grading_version, taxonomy_version, configuration) VALUES (%s,%s,%s)
        ON CONFLICT (grading_version) DO NOTHING''',
        (context.grading_version, context.taxonomy_version, Json(context.snapshot)))


def persist_grades(results, context, batch_id=None):
    """Append an audited grading run; transaction rollback preserves existing rows."""
    rows = list(results)
    connection = _connect(5, 30, 5)
    try:
        with connection, connection.cursor() as cursor:
            cursor.execute(SCHEMA_PATH.read_text(encoding='utf-8'))
            register_configuration(cursor, context)
            for result in rows:
                grade = result.deterministic_grade
                if (grade['grading_version'], grade['taxonomy_version']) != (context.grading_version, context.taxonomy_version):
                    raise ValueError('Grade versions do not match the configuration being persisted')
                key = make_job_key(result.source_site, result.id or None, result.source or None)
                cursor.execute('''INSERT INTO public.skill_scores
                    (batch_id, job_id, role, link, total_score, fit_band, matched_skills,
                     missing_skills, score_breakdown, flags, score_reason, created_at,
                     scoring_version, score_source, job_key, grading_version, taxonomy_version,
                     role_lane, lane_scores, fit_score, learning_score, pre_ai_score, confidence,
                     ai_review_required, deterministic_grade)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (batch_id, result.id, result.title, result.source, result.score, result.fit_quality,
                     Json(grade['matched_capability_concepts']), Json(grade['missing_required_skills']),
                     Json(grade['triggered_rules']), Json({'search_lane':result.search_lane}), result.reason_codes,
                     context.grading_version, 'deterministic', key, context.grading_version,
                     context.taxonomy_version, result.role_lane, Json(grade['lane_scores']),
                     grade['fit_score'], grade['learning_score'], grade['pre_ai_score'],
                     grade['confidence'], grade['ai_review_required'], Json(grade)))
    finally:
        connection.close()
    return len(rows)
