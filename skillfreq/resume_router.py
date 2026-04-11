from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Any
import re

from dotenv import load_dotenv
import pandas as pd
import yaml


load_dotenv()


@dataclass
class ResumeRecommendation:
    best_resume: str
    reason: str
    scores: dict[str, int]


def _normalize(text: Any) -> str:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    text = str(text).lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def load_roles_config(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("roles.yml must be a mapping")
    return data


def _count_terms(text: str, keywords: list[str]) -> int:
    return sum(1 for kw in keywords if kw.lower() in text)


def _description_first_bucket_score(title: str, description: str, keywords: list[str]) -> int:
    title_hits = _count_terms(title, keywords)
    desc_hits = _count_terms(description, keywords)
    return (desc_hits * 3) + title_hits


def _apply_title_bonus(scores: dict[str, int], title: str, config: dict[str, Any], bonus: int = 2) -> dict[str, int]:
    updated = scores.copy()
    overrides = config.get("title_overrides", {})

    for resume_name, keywords in overrides.items():
        if any(kw.lower() in title for kw in keywords):
            updated[resume_name] = updated.get(resume_name, 0) + bonus

    return updated

def _ai_stack_penalty(description: str, config: dict[str, Any]) -> int:
    penalty_cfg = config.get("ai_stack_penalty", {})
    keywords = penalty_cfg.get("keywords", [])
    base_penalty = penalty_cfg.get("penalty_score", 0)

    ai_hits = _count_terms(description, keywords)

    if ai_hits < 2:
        return 0

    return min(3, base_penalty + (ai_hits // 4))



def _seniority_penalty(title: str, description: str, config: dict[str, Any]) -> int:
    
    penalties = config.get("seniority_penalties", {})
    penalty = 0

    for kw in penalties.get("hard_titles", []):
        if kw.lower() in title:
            penalty += 3
            break

    for kw in penalties.get("medium_requirements", []):
        if kw.lower() in description:
            penalty += 2
            break

    return penalty


def _resolve_tie_with_content(full_text: str) -> str:
    if any(term in full_text for term in ["sql", "etl", "elt", "pipeline", "pipelines", "dbt", "airflow", "data warehouse"]):
        return "Engineer_Data"
    if any(term in full_text for term in ["dashboard", "reporting", "metrics", "bi", "business intelligence", "analytics"]):
        return "Engineer_Analytics"
    if any(term in full_text for term in ["ci/cd", "deployment", "observability", "reliability", "infrastructure", "platform"]):
        return "Engineer_Platform"
    return "Engineer_Software"


def suggest_resume_variant(
    title: str,
    description: str,
    roles_config: dict[str, Any],
) -> ResumeRecommendation:
    norm_title = _normalize(title)
    norm_desc = _normalize(description)
    full_text = f"{norm_title} {norm_desc}".strip()

    if not full_text:
        return ResumeRecommendation(
            best_resume="Engineer_Software",
            reason="Defaulted because title and description were empty.",
            scores={},
        )

    resume_variants = roles_config.get("resume_variants", {})
    negative_keywords = roles_config.get("negative_keywords", {})

    scores: dict[str, int] = {}
    for resume_name, meta in resume_variants.items():
        keywords = meta.get("keywords", [])
        base_score = _description_first_bucket_score(norm_title, norm_desc, keywords)
        neg_score = _count_terms(full_text, negative_keywords.get(resume_name, []))
        scores[resume_name] = base_score - neg_score


    seniority_penalty = _seniority_penalty(norm_title, norm_desc, roles_config)
    if seniority_penalty:
        for resume_name in scores:
            scores[resume_name] -= seniority_penalty
            
    ai_penalty = _ai_stack_penalty(norm_desc, roles_config)
    if ai_penalty:
        for resume_name in scores:
            scores[resume_name] -= ai_penalty


    scores = _apply_title_bonus(scores, norm_title, roles_config, bonus=2)

    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    best_resume = sorted_scores[0][0]
    top_score = sorted_scores[0][1]
    runner_up = sorted_scores[1] if len(sorted_scores) > 1 else None

    # If top two are tied or very close, let content decide
    if runner_up and (top_score - runner_up[1] <= 1):
        best_resume = _resolve_tie_with_content(full_text)

    top_keywords = resume_variants.get(best_resume, {}).get("keywords", [])
    matched_keywords = [kw for kw in top_keywords if kw.lower() in full_text][:4]

    reason_parts: list[str] = []

    if matched_keywords:
        reason_parts.append("JD matched " + ", ".join(matched_keywords))

    if any(
        kw.lower() in norm_title
        for keywords in roles_config.get("title_overrides", {}).values()
        for kw in keywords
    ):
        reason_parts.append("title used as soft tie-breaker")

    if seniority_penalty:
        reason_parts.append("seniority language detected")

    if not reason_parts:
        reason_parts.append("best overall JD lane match")

    return ResumeRecommendation(
        best_resume=best_resume,
        reason="; ".join(reason_parts).capitalize() + ".",
        scores=scores,
    )


def route_resumes_for_csv(
    input_csv: Path,
    out_csv: Path,
    roles_path: Path,
    title_col: str = "Role",
    jd_col: str = "JDText",
) -> pd.DataFrame:
    base_path = os.getenv("NOTION_TRACKER_PATH", "").strip('"')
    if not base_path:
        raise ValueError("Environment variable NOTION_TRACKER_PATH is not set.")

    path = os.path.join(base_path, str(input_csv))
    df = pd.read_csv(path)
    df.columns = [str(c).strip() for c in df.columns]

    roles_config = load_roles_config(roles_path)

    missing_cols = [col for col in [title_col, jd_col] if col not in df.columns]
    if missing_cols:
        raise ValueError(
            f"Missing required columns for resume routing: {missing_cols}. "
            f"Available columns: {list(df.columns)}"
        )

    recommendations = [
        suggest_resume_variant(row.get(title_col, ""), row.get(jd_col, ""), roles_config)
        for _, row in df.iterrows()
    ]

    df["recommended_resume"] = [r.best_resume for r in recommendations]
    df["resume_reason"] = [r.reason for r in recommendations]
    df["lane_score_data"] = [r.scores.get("Engineer_Data", 0) for r in recommendations]
    df["lane_score_analytics"] = [r.scores.get("Engineer_Analytics", 0) for r in recommendations]
    df["lane_score_platform"] = [r.scores.get("Engineer_Platform", 0) for r in recommendations]
    df["lane_score_software"] = [r.scores.get("Engineer_Software", 0) for r in recommendations]

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    return df