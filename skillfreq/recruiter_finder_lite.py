# recruiter_finder_lite.py
# Adds recruiter/contact search fields to your Job Tracker CSV.
import pandas as pd
from urllib.parse import quote
from pathlib import Path
import os
import re
from dotenv import load_dotenv
load_dotenv()

#currently hardcoded to my Job Tracker from Notion export - update as needed
INPUT_FILE = os.getenv("NOTION_TRACKER_PATH") + "\\"+"outreach-5-8-26.csv"
OUTPUT_FILE = "job_tracker_with_recruiter_finder-5-8-26.csv"


def get_col(row, possible_names):
    for name in possible_names:
        if name in row and pd.notna(row[name]):
            return str(row[name]).strip()
    return ""


def linkedin_recruiter_search_url(company, company_id=""):
    keywords = quote("technical recruiters ", safe="")

    if company_id:
        current_company = quote(f'["{company_id}"]', safe="")
        return (
            "https://www.linkedin.com/search/results/people/"
            f"?keywords={keywords}&origin=FACETED_SEARCH&currentCompany={current_company}"
        )

    search_terms = quote(f"technical recruiters {company}", safe="")
    return (
        "https://www.linkedin.com/search/results/people/"
        f"?keywords={search_terms}&origin=FACETED_SEARCH"
    )


def extract_linkedin_company_id(*values):
    for value in values:
        match = re.search(r"currentCompany=%5B%22(\d+)%22%5D", value)
        if match:
            return match.group(1)

        match = re.search(r"linkedin\.com/company/(\d+)", value)
        if match:
            return match.group(1)

        if value.isdigit():
            return value

    return ""


def build_queries(company, role, company_id=""):
    return {
        "LinkedIn Technical Recruiter Search URL": linkedin_recruiter_search_url(company, company_id),
    }


def should_check_contact(row):
    fit = get_col(row, ["Manual FIT (1-5)"]).lower()
    status = get_col(row, ["Status"]).lower()
    pivot = get_col(row, ["Pivotable?"]).lower()

    weak_signals = [
        "weak" in fit,
        "skip" in status,
        "rejected" in status,
        "denied" in status,
        "risky" in pivot,
        "not" in pivot,
    ]

    strong_signals = [
        "good" in fit,
        "submitted" in status,
        "applied" in status,
        "pivotable" in pivot,
        "pivot-safe" in pivot,
        "safe" in pivot,
    ]

    if any(weak_signals):
        return "skip"

    if any(strong_signals):
        return "check"

    return "optional"


def main():
    input_path = Path(INPUT_FILE)

    if not input_path.exists():
        raise FileNotFoundError(f"Could not find input file: {INPUT_FILE}")

    df = pd.read_csv(input_path)

    results = []

    for _, row in df.iterrows():
        company = get_col(row, ["Company", "company", "company_name", "employer"])
        role = get_col(row, ["Role", "title", "role_title", "job_title", "Job Title"])
        job_url = get_col(row, ["Link", "job_url", "Job URL"])
        company_id = get_col(row, [
            "LinkedIn Company ID",
            "Company LinkedIn ID",
            "linkedin_company_id",
            "currentCompany",
        ])
        company_id = extract_linkedin_company_id(company_id, company, job_url)

        if not company:
            queries = {}
            contact_priority = "missing_company"
        else:
            queries = build_queries(company, role, company_id)
            contact_priority = should_check_contact(row)

        results.append({
            "Contact Priority": contact_priority,
            "Contact Status": "not_checked",
            "Contact Name": "",
            "Contact Title": "",
            "Contact Profile URL": "",
            "Contacted Date": "",
            "Follow Up Date": "",
            "Contact Notes": "",
            "Original Job URL": job_url,
            **queries,
        })

    recruiter_df = pd.DataFrame(results)
    final_df = pd.concat([df, recruiter_df], axis=1)

    final_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Done. Created: {OUTPUT_FILE}")
    print("Recommended workflow: only check rows where Contact Priority == 'check'")


if __name__ == "__main__":
    main()
