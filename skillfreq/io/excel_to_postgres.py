from __future__ import annotations

import ast
import os
import re
from dataclasses import dataclass
from datetime import datetime
import logging
from pathlib import Path
from typing import Iterable, Sequence

import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2.extras import Json, execute_values


HEADER_RE = re.compile(r"[^a-z0-9_]+")
BASE_DIR = Path(__file__).resolve().parent.parent.parent
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoadResult:
    table: str
    rows: int
    columns: list[str]
    mode: str
    log_file: Path | None = None


@dataclass(frozen=True)
class FolderLoadResult:
    table: str
    files: int
    rows: int
    loaded_files: list[Path]
    mode: str
    log_file: Path | None = None


@dataclass(frozen=True)
class BatchImportResult:
    batch_id: str
    raw_jobs: int
    skill_scores: int
    calibration_results: int
    calibration_run_id: int | None
    log_file: Path | None = None


def configure_excel_load_logging(log_file: Path | None = None) -> Path:
    if log_file is None:
        log_dir = BASE_DIR / "logging"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = log_dir / f"excel_load_{timestamp}.log"

    log_file.parent.mkdir(parents=True, exist_ok=True)
    resolved_log_file = log_file.resolve()

    for handler in logger.handlers:
        if getattr(handler, "baseFilename", None) == str(resolved_log_file):
            return resolved_log_file

    file_handler = logging.FileHandler(resolved_log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    logger.info("Excel load logging initialized: %s", resolved_log_file)
    return resolved_log_file


def clean_value(value: object) -> object | None:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()
    return value


def text_value(row: pd.Series, column: str) -> str | None:
    value = clean_value(row.get(column))
    if value is None:
        return None
    return str(value)


def numeric_value(row: pd.Series, column: str) -> float | None:
    value = clean_value(row.get(column))
    if value is None:
        return None
    return float(value)


def int_value(row: pd.Series, column: str) -> int | None:
    value = clean_value(row.get(column))
    if value is None:
        return None
    return int(value)


def bool_value(row: pd.Series, column: str) -> bool | None:
    value = clean_value(row.get(column))
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def date_value(row: pd.Series, column: str):
    value = clean_value(row.get(column))
    if value is None:
        return None
    parsed = pd.to_datetime(value, errors="coerce")
    if pd.isna(parsed):
        return None
    return parsed.date()


def jsonish_value(value: object) -> object:
    value = clean_value(value)
    if value is None:
        return {}
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return {}
        try:
            return ast.literal_eval(stripped)
        except (ValueError, SyntaxError):
            return stripped
    return value


def listish_value(value: object) -> list[str]:
    value = clean_value(value)
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [part.strip() for part in str(value).split(",") if part.strip()]


def was_kept_value(value: object) -> bool | None:
    decision = clean_value(value)
    if decision is None:
        return None
    normalized = str(decision).strip().lower()
    if normalized in {"skip", "do_not_apply", "do not apply", "reject", "remove"}:
        return False
    return True


def normalize_header(value: object) -> str:
    raw = str(value or "").strip().lower()
    raw = raw.replace("%", " percent ")
    raw = HEADER_RE.sub("_", raw)
    raw = re.sub(r"_+", "_", raw).strip("_")
    return raw or "column"


def normalize_headers(headers: Iterable[object]) -> list[str]:
    counts: dict[str, int] = {}
    normalized: list[str] = []

    for header in headers:
        base = normalize_header(header)
        count = counts.get(base, 0)
        counts[base] = count + 1
        normalized.append(base if count == 0 else f"{base}_{count + 1}")

    return normalized


def parse_table_name(table: str, default_schema: str = "public") -> tuple[str, str]:
    parts = [part.strip() for part in table.split(".") if part.strip()]
    if len(parts) == 1:
        return default_schema, parts[0]
    if len(parts) == 2:
        return parts[0], parts[1]
    raise ValueError("Table must be in the form table_name or schema.table_name")


def connect():
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        logger.info("Connecting to PostgreSQL using DATABASE_URL")
        return psycopg2.connect(database_url)

    logger.info(
        "Connecting to PostgreSQL using DB_NAME/DB_USER/DB_HOST/DB_PORT env vars: host=%s port=%s db=%s user=%s",
        os.getenv("DB_HOST", "localhost"),
        os.getenv("DB_PORT", "5432"),
        os.getenv("DB_NAME"),
        os.getenv("DB_USER"),
    )
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
    )


def read_excel(path: Path, sheet_name: str | int | None = 0) -> pd.DataFrame:
    """Read either an Excel workbook or a CSV export into a normalized frame."""
    suffix = path.suffix.lower()
    logger.info("Reading tabular file: path=%s sheet=%s", path, sheet_name)

    if suffix == ".csv":
        # JobSpy CSV exports may contain a UTF-8 BOM and multiline descriptions.
        df = pd.read_csv(path, encoding="utf-8-sig", low_memory=False)
    elif suffix in {".xlsx", ".xls", ".xlsm"}:
        df = pd.read_excel(path, sheet_name=sheet_name)
    else:
        raise ValueError(
            f"Unsupported input file type '{suffix or '<none>'}'; expected .csv, .xlsx, .xls, or .xlsm"
        )

    if isinstance(df, dict):
        df = next(iter(df.values()))
        logger.info("Multiple sheets returned; using the first sheet")
    df = df.dropna(how="all")
    original_columns = [str(column) for column in df.columns]
    df.columns = normalize_headers(df.columns)
    # Preserve useful PostgreSQL types for the standard jobs-M-D-YY.csv format.
    if suffix == ".csv":
        if "date_posted" in df.columns:
            df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
        if "is_remote" in df.columns:
            normalized = df["is_remote"].astype("string").str.strip().str.lower()
            df["is_remote"] = normalized.map(
                {"true": True, "false": False, "1": True, "0": False, "yes": True, "no": False}
            ).astype("boolean")

    logger.info("Read %s rows and %s columns", len(df), len(df.columns))
    logger.info("Normalized columns: %s", ", ".join(df.columns))
    if original_columns != list(df.columns):
        logger.info("Original columns: %s", ", ".join(original_columns))
    return df


def read_review_sheet(path: Path, sheet_name: str = "Base") -> pd.DataFrame:
    logger.info("Reading review workbook: path=%s sheet=%s", path, sheet_name)
    df = pd.read_excel(path, sheet_name=sheet_name)
    df = df.dropna(how="all")
    logger.info("Read %s review row(s) from sheet %s", len(df), sheet_name)
    return df


def infer_postgres_type(series: pd.Series) -> str:
    # pandas represents a completely empty CSV column as float64. Treating that
    # as a database type is unsafe because a later file may contain text there.
    if series.isna().all():
        return "TEXT"
    if pd.api.types.is_bool_dtype(series):
        return "BOOLEAN"
    if pd.api.types.is_integer_dtype(series):
        return "BIGINT"
    if pd.api.types.is_float_dtype(series):
        return "DOUBLE PRECISION"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "TIMESTAMPTZ"
    return "TEXT"


def create_table_statement(
    schema: str,
    table: str,
    df: pd.DataFrame,
    primary_key: Sequence[str] | None = None,
) -> sql.Composed:
    column_defs = [
        sql.SQL("{} {}").format(sql.Identifier(column), sql.SQL(infer_postgres_type(df[column])))
        for column in df.columns
    ]

    if primary_key:
        missing = sorted(set(primary_key) - set(df.columns))
        if missing:
            raise ValueError(f"Primary key column(s) not found in Excel data: {', '.join(missing)}")
        column_defs.append(
            sql.SQL("PRIMARY KEY ({})").format(
                sql.SQL(", ").join(sql.Identifier(column) for column in primary_key)
            )
        )

    return sql.SQL("CREATE TABLE IF NOT EXISTS {}.{} ({})").format(
        sql.Identifier(schema),
        sql.Identifier(table),
        sql.SQL(", ").join(column_defs),
    )


def rows_for_insert(df: pd.DataFrame) -> list[tuple[object, ...]]:
    prepared = df.astype(object).where(pd.notnull(df), None)
    return [tuple(row) for row in prepared.to_numpy()]


def insert_statement(
    schema: str,
    table: str,
    columns: Sequence[str],
    mode: str,
    primary_key: Sequence[str] | None = None,
) -> sql.Composed:
    base = sql.SQL("INSERT INTO {}.{} ({}) VALUES %s").format(
        sql.Identifier(schema),
        sql.Identifier(table),
        sql.SQL(", ").join(sql.Identifier(column) for column in columns),
    )

    if mode != "upsert":
        return base

    if not primary_key:
        raise ValueError("--primary-key is required when --mode upsert is used")

    update_columns = [column for column in columns if column not in primary_key]
    if not update_columns:
        return base + sql.SQL(" ON CONFLICT ({}) DO NOTHING").format(
            sql.SQL(", ").join(sql.Identifier(column) for column in primary_key)
        )

    return base + sql.SQL(" ON CONFLICT ({}) DO UPDATE SET {}").format(
        sql.SQL(", ").join(sql.Identifier(column) for column in primary_key),
        sql.SQL(", ").join(
            sql.SQL("{} = EXCLUDED.{}").format(sql.Identifier(column), sql.Identifier(column))
            for column in update_columns
        ),
    )


def load_excel_to_postgres(
    excel_path: Path,
    table_name: str,
    sheet_name: str | int | None = 0,
    mode: str = "append",
    primary_key: Sequence[str] | None = None,
    schema: str = "public",
    log_file: Path | None = None,
    dataframe: pd.DataFrame | None = None,
) -> LoadResult:
    resolved_log_file = configure_excel_load_logging(log_file)
    logger.info(
        "Starting Excel load: excel=%s table=%s sheet=%s mode=%s primary_key=%s schema=%s",
        excel_path,
        table_name,
        sheet_name,
        mode,
        list(primary_key or []),
        schema,
    )

    if mode not in {"append", "replace", "upsert"}:
        raise ValueError("mode must be append, replace, or upsert")

    try:
        df = dataframe if dataframe is not None else read_excel(excel_path, sheet_name=sheet_name)
        resolved_schema, table = parse_table_name(table_name, default_schema=schema)
        primary_key = list(primary_key or [])
        rows = rows_for_insert(df)
        logger.info("Resolved destination table: %s.%s", resolved_schema, table)
        logger.info("Prepared %s row(s) for insert", len(rows))

        with connect() as conn:
            with conn.cursor() as cur:
                logger.info("Ensuring schema exists: %s", resolved_schema)
                cur.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(resolved_schema)))

                if mode == "replace":
                    logger.info("Dropping destination table before replace: %s.%s", resolved_schema, table)
                    cur.execute(
                        sql.SQL("DROP TABLE IF EXISTS {}.{}").format(
                            sql.Identifier(resolved_schema),
                            sql.Identifier(table),
                        )
                    )

                logger.info("Ensuring destination table exists")
                cur.execute(create_table_statement(resolved_schema, table, df, primary_key))

                if rows:
                    logger.info("Writing rows to PostgreSQL")
                    execute_values(
                        cur,
                        insert_statement(resolved_schema, table, list(df.columns), mode, primary_key).as_string(cur),
                        rows,
                    )
                else:
                    logger.info("No rows found after dropping blank Excel rows; table was still ensured")

        logger.info("Completed Excel load: rows=%s table=%s.%s mode=%s", len(rows), resolved_schema, table, mode)
    except Exception:
        logger.exception("Excel load failed")
        raise

    return LoadResult(
        table=f"{resolved_schema}.{table}",
        rows=len(rows),
        columns=list(df.columns),
        mode=mode,
        log_file=resolved_log_file,
    )


def load_csv_folder_to_postgres(
    folder_path: Path,
    table_name: str,
    mode: str = "append",
    primary_key: Sequence[str] | None = None,
    schema: str = "public",
    log_file: Path | None = None,
) -> FolderLoadResult:
    """Load every CSV beneath a folder into the same PostgreSQL table."""
    if not folder_path.is_dir():
        raise ValueError(f"CSV folder does not exist or is not a directory: {folder_path}")

    csv_files = sorted(
        (path for path in folder_path.rglob("*") if path.is_file() and path.suffix.lower() == ".csv"),
        key=lambda path: str(path.relative_to(folder_path)).lower(),
    )
    if not csv_files:
        raise ValueError(f"No CSV files found under: {folder_path}")

    resolved_log_file = configure_excel_load_logging(log_file)
    logger.info(
        "Starting CSV folder load: folder=%s files=%s table=%s mode=%s",
        folder_path,
        len(csv_files),
        table_name,
        mode,
    )

    # Infer the table from the complete folder rather than the first file.
    # JobSpy has added columns over time, and columns that are blank in one
    # export can contain text in another.
    frames: list[pd.DataFrame] = []
    for index, csv_file in enumerate(csv_files):
        logger.info("Reading CSV %s of %s for unified schema: %s", index + 1, len(csv_files), csv_file)
        frame = read_excel(csv_file)
        frame["source_file"] = csv_file.name
        frames.append(frame)

    combined_df = pd.concat(frames, ignore_index=True, sort=False)
    logger.info(
        "Unified folder data contains %s rows and %s columns",
        len(combined_df),
        len(combined_df.columns),
    )
    result = load_excel_to_postgres(
        excel_path=folder_path,
        table_name=table_name,
        mode=mode,
        primary_key=primary_key,
        schema=schema,
        log_file=resolved_log_file,
        dataframe=combined_df,
    )
    total_rows = result.rows
    resolved_table = result.table

    logger.info(
        "Completed CSV folder load: files=%s rows=%s table=%s",
        len(csv_files),
        total_rows,
        resolved_table,
    )
    return FolderLoadResult(
        table=resolved_table,
        files=len(csv_files),
        rows=total_rows,
        loaded_files=csv_files,
        mode=mode,
        log_file=resolved_log_file,
    )


def replace_batch(cur, batch_id: str) -> None:
    logger.info("Replacing existing rows for batch_id=%s", batch_id)
    cur.execute(
        sql.SQL(
            """
            DELETE FROM calibration_results
            WHERE batch_id = %s
               OR calibration_run_id IN (SELECT id FROM calibration_runs WHERE batch_id = %s)
            """
        ),
        (batch_id, batch_id),
    )
    cur.execute("DELETE FROM calibration_runs WHERE batch_id = %s", (batch_id,))
    cur.execute("DELETE FROM skill_scores WHERE batch_id = %s", (batch_id,))
    cur.execute("DELETE FROM raw_jobs WHERE batch_id = %s", (batch_id,))


def insert_raw_jobs(cur, jobs_df: pd.DataFrame, batch_id: str, source_file_name: str) -> dict[str, int]:
    rows = []
    for _, row in jobs_df.iterrows():
        rows.append(
            (
                batch_id,
                text_value(row, "id"),
                text_value(row, "site"),
                text_value(row, "company"),
                text_value(row, "title"),
                text_value(row, "location"),
                text_value(row, "job_url"),
                text_value(row, "description"),
                date_value(row, "date_posted"),
                None,
                text_value(row, "search_term_used"),
                bool_value(row, "is_remote"),
                text_value(row, "job_type"),
                numeric_value(row, "min_amount"),
                numeric_value(row, "max_amount"),
                source_file_name,
                "jobspy_csv",
            )
        )

    if not rows:
        return {}

    returned = execute_values(
        cur,
        """
        INSERT INTO raw_jobs (
            batch_id, job_id, source_site, company, title, location, job_url,
            description_raw, date_posted, scraped_at, search_keyword, is_remote,
            employment_type, salary_min, salary_max, source_file_name, created_at, ingest_type
        )
        VALUES %s
        RETURNING job_id, id
        """,
        [row[:-1] + (datetime.now(), row[-1]) for row in rows],
        fetch=True,
    )
    return {job_id: raw_id for job_id, raw_id in returned if job_id}


def insert_skill_scores(
    cur,
    scores_df: pd.DataFrame,
    raw_job_ids: dict[str, int],
    raw_lookup: pd.DataFrame,
    batch_id: str,
    scoring_version: str,
) -> int:
    raw_by_job_id = raw_lookup.set_index("id", drop=False) if "id" in raw_lookup.columns else pd.DataFrame()
    rows = []

    for _, row in scores_df.iterrows():
        job_id = text_value(row, "id")
        raw_job_id = raw_job_ids.get(job_id or "")
        raw_row = raw_by_job_id.loc[job_id] if job_id in raw_by_job_id.index else None
        company = clean_value(raw_row.get("company")) if raw_row is not None else None
        score_breakdown = jsonish_value(row.get("matches"))
        flags = {
            "raw_match": text_value(row, "raw_match"),
            "role_lane": text_value(row, "role_lane"),
            "apply_decision": text_value(row, "apply_decision"),
            "search_lane": text_value(row, "search_lane"),
            "search_term_used": text_value(row, "search_term_used"),
            "review_priority": int_value(row, "review_priority"),
            "matched": int_value(row, "matched"),
            "required_total": int_value(row, "required_total"),
        }

        rows.append(
            (
                batch_id,
                job_id,
                raw_job_id,
                company,
                text_value(row, "title"),
                text_value(row, "source"),
                numeric_value(row, "score"),
                text_value(row, "fit_quality"),
                Json(score_breakdown),
                Json(listish_value(row.get("missing"))),
                Json(score_breakdown),
                Json({k: v for k, v in flags.items() if v is not None}),
                text_value(row, "reason_codes"),
                scoring_version,
                "skillfreq_csv",
            )
        )

    if not rows:
        return 0

    execute_values(
        cur,
        """
        INSERT INTO skill_scores (
            batch_id, job_id, raw_job_id, company, role, link, total_score,
            fit_band, matched_skills, missing_skills, score_breakdown, flags,
            score_reason, created_at, scoring_version, score_source
        )
        VALUES %s
        """,
        [row[:-2] + (datetime.now(), row[-2], row[-1]) for row in rows],
    )
    return len(rows)


def insert_calibration_run(
    cur,
    batch_id: str,
    run_name: str,
    review_xlsx: Path,
    jobs_input: int,
    jobs_output: int,
    jobs_removed: int,
    scoring_version: str,
    rules_version: str,
    run_notes: str | None,
) -> int:
    cur.execute(
        """
        INSERT INTO calibration_runs (
            batch_id, run_name, scripted_name, scripted_version, rules_version,
            scoring_version, input_source, input_file_name, output_file_name,
            jobs_input, jobs_output, jobs_removed, run_notes, created_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            batch_id,
            run_name,
            "skillfreq_import_batch",
            "1",
            rules_version,
            scoring_version,
            "review_workbook",
            review_xlsx.name,
            review_xlsx.name,
            jobs_input,
            jobs_output,
            jobs_removed,
            run_notes,
            datetime.now(),
        ),
    )
    return int(cur.fetchone()[0])


def insert_calibration_results(
    cur,
    review_df: pd.DataFrame,
    raw_job_ids: dict[str, int],
    raw_lookup: pd.DataFrame,
    batch_id: str,
    calibration_run_id: int,
    cleaning_version: str,
) -> int:
    raw_by_job_id = raw_lookup.set_index("id", drop=False) if "id" in raw_lookup.columns else pd.DataFrame()
    rows = []
    for _, row in review_df.iterrows():
        job_id = text_value(row, "id") or text_value(row, "Order")
        if not job_id:
            continue
        raw_row = raw_by_job_id.loc[job_id] if job_id in raw_by_job_id.index else None
        company = clean_value(raw_row.get("company")) if raw_row is not None else None
        role = text_value(row, "title") or (clean_value(raw_row.get("title")) if raw_row is not None else None)
        link = text_value(row, "source") or (clean_value(raw_row.get("job_url")) if raw_row is not None else None)
        rows.append(
            (
                calibration_run_id,
                batch_id,
                job_id,
                raw_job_ids.get(job_id),
                company,
                role,
                link,
                was_kept_value(row.get("Apply Decision")),
                numeric_value(row, "score"),
                text_value(row, "Fit Quality"),
                Json(jsonish_value(row.get("matches"))),
                Json(
                    {
                        "skillfreq_fit_quality": text_value(row, "fit_quality"),
                        "skillfreq_role_lane": text_value(row, "role_lane"),
                        "skillfreq_apply_decision": text_value(row, "apply_decision"),
                        "ai_role_lane": text_value(row, "Role Lane"),
                        "ai_reason": text_value(row, "Reason"),
                        "raw_match": text_value(row, "raw_match"),
                        "missing": listish_value(row.get("missing")),
                        "matched": int_value(row, "matched"),
                        "required_total": int_value(row, "required_total"),
                    }
                ),
                text_value(row, "Reason"),
                datetime.now(),
                cleaning_version,
            )
        )

    if not rows:
        return 0

    execute_values(
        cur,
        """
        INSERT INTO calibration_results (
            calibration_run_id, batch_id, job_id, raw_job_id, company, role, link,
            was_kept, skillfreq_score, fit_band, score_breakdown, flags,
            calibration_notes, created_at, cleaning_version
        )
        VALUES %s
        """,
        rows,
    )
    return len(rows)


def import_skillfreq_batch(
    jobs_csv: Path,
    scores_csv: Path,
    review_xlsx: Path | None,
    batch_id: str,
    review_sheet: str = "Base",
    batch_mode: str = "append",
    scoring_version: str = "unknown",
    rules_version: str = "unknown",
    cleaning_version: str = "unknown",
    run_name: str | None = None,
    run_notes: str | None = None,
    log_file: Path | None = None,
) -> BatchImportResult:
    if batch_mode not in {"append", "replace"}:
        raise ValueError("batch_mode must be append or replace")

    resolved_log_file = configure_excel_load_logging(log_file)
    logger.info(
        "Starting SkillFreq batch import: batch_id=%s jobs_csv=%s scores_csv=%s review_xlsx=%s",
        batch_id,
        jobs_csv,
        scores_csv,
        review_xlsx,
    )

    jobs_df = pd.read_csv(jobs_csv)
    scores_df = pd.read_csv(scores_csv)
    review_df = read_review_sheet(review_xlsx, review_sheet) if review_xlsx else None
    logger.info("Loaded source files: raw_jobs=%s skill_scores=%s", len(jobs_df), len(scores_df))

    calibration_run_id = None
    calibration_count = 0

    try:
        with connect() as conn:
            with conn.cursor() as cur:
                if batch_mode == "replace":
                    replace_batch(cur, batch_id)

                raw_job_ids = insert_raw_jobs(cur, jobs_df, batch_id, jobs_csv.name)
                logger.info("Inserted %s raw job row(s)", len(raw_job_ids))

                skill_count = insert_skill_scores(
                    cur,
                    scores_df,
                    raw_job_ids,
                    jobs_df,
                    batch_id,
                    scoring_version,
                )
                logger.info("Inserted %s skill score row(s)", skill_count)

                if review_xlsx and review_df is not None:
                    calibration_run_id = insert_calibration_run(
                        cur,
                        batch_id=batch_id,
                        run_name=run_name or f"{batch_id} calibration",
                        review_xlsx=review_xlsx,
                        jobs_input=len(jobs_df),
                        jobs_output=len(scores_df),
                        jobs_removed=max(len(jobs_df) - len(scores_df), 0),
                        scoring_version=scoring_version,
                        rules_version=rules_version,
                        run_notes=run_notes,
                    )
                    calibration_count = insert_calibration_results(
                        cur,
                        review_df,
                        raw_job_ids,
                        jobs_df,
                        batch_id,
                        calibration_run_id,
                        cleaning_version,
                    )
                    logger.info(
                        "Inserted calibration run %s with %s result row(s)",
                        calibration_run_id,
                        calibration_count,
                    )

        logger.info("Completed SkillFreq batch import: batch_id=%s", batch_id)
    except Exception:
        logger.exception("SkillFreq batch import failed")
        raise

    return BatchImportResult(
        batch_id=batch_id,
        raw_jobs=len(jobs_df),
        skill_scores=len(scores_df),
        calibration_results=calibration_count,
        calibration_run_id=calibration_run_id,
        log_file=resolved_log_file,
    )
